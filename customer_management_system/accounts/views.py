from django.shortcuts import render
from django.http import HttpResponse
from .models import *
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

def customer(request):
    return render(request, 'accounts/customer.html')