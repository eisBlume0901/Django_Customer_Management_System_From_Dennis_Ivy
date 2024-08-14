from django.urls import path
from . import views 
# from .views import RegisterView

# https://docs.djangoproject.com/en/5.0/topics/http/urls/
# Every url must end with a slash
urlpatterns = [
    path('register/', views.register, name="register"),
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name="logout"),

    path('', views.home, name="home"),
    path('products/', views.products, name="products"),
    # pk means primary key, it is a parameter to be passed to the view
    # The view will then use this parameter to query the database
    # Purpose is for dynamic routing
    path('user/<int:pk>/profile', views.userProfileSettings, name="userProfileSettings"),

    path('user/<int:pk>', views.userHome, name="userPage"),
    path('customer/<str:pk>/', views.customer, name="customer"),
    path('update_customer/<str:pk>/', views.updateCustomer, name="update_customer"),
    path('create_order/<str:pk>/', views.createOrder, name="create_order"),
    path('update_order/<str:pk>/', views.updateOrder, name="update_order"),
    path('delete_order/<str:pk>/', views.deleteOrder, name="delete_order"),
]