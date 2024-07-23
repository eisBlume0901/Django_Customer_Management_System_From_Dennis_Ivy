from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('products/', views.products),
    # pk means primary key, it is a parameter to be passed to the view
    # The view will then use this parameter to query the database
    # Purpose is for dynamic routing
    path('customer/<str:pk>', views.customer),
]