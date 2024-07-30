from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.urls import reverse
from .models import *

from .forms import * # Means that we are importing that Form class from the forms.py file
from django.forms import inlineformset_factory # Allows creation of multiple forms with single submit button (so that you can do mass creation and updates of data)

from .filters import *
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout

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
            orders = form.save()
            for order in orders:
                messages.success(request, f'{order.product.name} was created successfully for {customer.name}')
            return redirect(reverse('home')) # Redirect using the name of the url (instead of the route path)

    context = {
        'formset': formset,
        'is_update': False,
    }
    return render(request, 'forms/order_form.html', context)

def updateOrder(request, pk):
    order = get_object_or_404(Order, id=pk)
    customer = order.customer
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=0)
    formset = OrderFormSet(queryset=Order.objects.filter(id=pk), instance=customer)

    if request.method == 'POST':
        formset = OrderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            messages.success(request, f'Order was updated successfully for {customer.name}')
            return redirect(reverse('home'))
       

    context = {
        'formset': formset,
        'is_update': True,
    }
    return render(request, 'forms/order_form.html', context)

def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)

    if request.method == 'POST':
        order.delete()
        messages.success(request, f'Order was deleted successfully for {order.customer.name}')
        return redirect(reverse('home'))
    
    context = {
        'order' : order,

    }
    return render(request, 'forms/delete_form.html', context)


def register(request):
    form = RegisterUserForm()
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, f'Account was created successfully! for {user}') # This is only seen at 127.0.0.1:800/admin (or admin panel)
            return redirect(reverse('login'))
        else:
            messages.error(request, 'There was an error creating the account. Please check the form for errors.')
    return render(request, 'forms/register.html', {'form': form})

def login(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                messages.success(request, f'Welcome {username}!')
                return redirect(reverse('home'))
        else:
            messages.error(request, 'Invalid user and password. Please try again!')

    return render(request, 'forms/login.html', {'form': form})

def logout(request):
    auth_logout(request)
    return redirect(reverse('login'))