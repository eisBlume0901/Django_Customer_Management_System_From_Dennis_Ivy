from django.forms import ModelForm
from . models import *
from django import forms


class OrderForm(ModelForm):
    class Meta:
        # Specify two things: model and fields
        model = Order
        fields = '__all__' # specifies that all the attributes in the Order model will be included in the form
        # For specifity, the syntax is: fields = ['customer', 'product', 'status']