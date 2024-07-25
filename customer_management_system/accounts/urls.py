from django.urls import path
from . import views

# https://docs.djangoproject.com/en/5.0/topics/http/urls/
# Every url must end with a slash
urlpatterns = [
    path('', views.home, name="home"),
    path('products/', views.products, name="products"),
    # pk means primary key, it is a parameter to be passed to the view
    # The view will then use this parameter to query the database
    # Purpose is for dynamic routing
    path('customer/<str:pk>/', views.customer, name="customer"),
    path('create_order/', views.createOrder, name="create_order"),
    path('update_order/<str:pk>/', views.updateOrder, name="update_order"),
    path('delete_order/<str:pk>/', views.deleteOrder, name="delete_order"),
]