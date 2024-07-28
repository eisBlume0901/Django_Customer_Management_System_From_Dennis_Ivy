from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from .models import *

from .forms import * # Means that we are importing that Form class from the forms.py file
from django.forms import inlineformset_factory # Allows creation of multiple forms with single submit button (so that you can do mass creation and updates of data)

from .filters import *


# Create your views here.
def home(request):
    allOrders = Order.objects.all()
    allCustomers = Customer.objects.all()
    allPendingOrders = Order.objects.filter(status="Pending").count()
    allOutOfDeliveryOrders = Order.objects.filter(status="Out for delivery").count()
    allDeliveredOrders = Order.objects.filter(status="Delivered").count()
    allOrdersCount = Order.objects.count()

    context = {
        'orders': allOrders,
        'ordersCount': allOrdersCount,
        'customers': allCustomers,
        'pendingOrders': allPendingOrders,
        'outOfDeliveryOrders': allOutOfDeliveryOrders,
        'deliveredOrders': allDeliveredOrders,
    }

    return render(request, 'accounts/dashboard.html', context)

def products(request):
    allProducts = Product.objects.all()
    return render(request, 'accounts/products.html', {'products': allProducts})

# pk means primary key
def customer(request, pk):
    customer = Customer.objects.get(id=pk)
    orders = customer.order_set.all()
    ordersCount = orders.count()

    orderFilter = OrderFilter(request.GET, queryset=orders)
    orders = orderFilter.qs # From all possible existing orders to filtered order
    
    context = {
        'customer': customer,
        'orders': orders,
        'ordersCount': ordersCount,
        'orderFilter': orderFilter,
    }
    return render(request, 'accounts/customer.html', context)

def createOrder(request, pk):

    # Have to declare the parent model first and then the child model (if there is a foreign key relationship)
    # If there is no parent-child relationship, then you can just declare the child model (or the model that you want to create a form for)
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=10) # extra is the number of forms that you want to display
    customer = Customer.objects.get(id=pk)

    # queryset=Order.objects.none() is used to prevent the form from displaying any existing data (since we are creating a new form)
    # It should belong to updateOrder function if we want to display existing data
    formset = OrderFormSet(queryset=Order.objects.none(),instance=customer) # For multiple forms, we use formset instead of form


    if request.method == 'POST':
        # print("Printing POST:", request.POST) # For debugging purposes

        form = OrderFormSet(request.POST, instance=customer) # For multiple forms, we use formset instead of form (and we pass the instance of the parent model so that the child model can be created)
        if form.is_valid():
            form.save()
            return redirect(reverse('home')) # Redirect using the name of the url (instead of the route path)
        
    context = {
        'formset': formset,
    }
    return render(request, 'forms/order_form.html', context)

def updateOrder(request, pk):

    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)

    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)

    if form.is_valid():
        form.save()
        return redirect(reverse('home')) 
    
    context = {
        'form': form,
    }

    return render(request, 'forms/order_form.html', context)

def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)

    if request.method == 'POST':
        order.delete()
        return redirect(reverse('home'))
    
    context = {
        'order' : order,

    }
    return render(request, 'forms/delete_form.html', context)

def register(request):
    form = RegisterUserForm()
    context = {
        'form': form,
    }

    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
         
    return render(request, 'forms/register.html', context)

def login(request):
    return render(request, 'forms/login.html')