from django.shortcuts import render
from django.http import HttpResponse
from .models import *
# Create your views here.
def home(request):
    allOrders = Order.objects.all()
    allCustomers = Customer.objects.all()

    context = {
        'orders': allOrders,
        'customers': allCustomers
    }

    return render(request, 'accounts/dashboard.html', context)

def products(request):
    allProducts = Product.objects.all()
    return render(request, 'accounts/products.html', {'products': allProducts})

def customer(request):
    return render(request, 'accounts/customer.html')