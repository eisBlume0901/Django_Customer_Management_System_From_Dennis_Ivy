from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from .models import *

from .forms import * # Means that we are importing that Form class from the forms.py file
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
    context = {
        'customer': customer,
        'orders': orders,
        'ordersCount': ordersCount,
    }
    return render(request, 'accounts/customer.html', context)

def createOrder(request, pk):

    customer = Customer.objects.get(id=pk)
    form = OrderForm(initial={'customer': customer})

    if request.method == 'POST':
        # print("Printing POST:", request.POST) # For debugging purposes

        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/') # Redirect using the name of the url (instead of the route path)
        
    context = {
        'form': form,
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