from django.forms import ModelForm
from . models import *
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User # Built-in User model

class OrderForm(ModelForm):
    class Meta:
        # Specify two things: model and fields
        model = Order
        fields = '__all__' # specifies that all the attributes in the Order model will be included in the form
        # For specifity, the syntax is: fields = ['customer', 'product', 'status']

class RegisterUserForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['first_name', 'last_name','username', 'email', 'password1', 'password2']

class AuthenticateUserForm(AuthenticationForm):

    class Meta:
        model = User
        fields = ['username', 'password']

class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
        exclude = ['date_created']

