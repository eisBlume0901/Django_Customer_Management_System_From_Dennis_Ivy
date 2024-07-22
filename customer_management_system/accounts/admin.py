from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Customer) # This will be present in the admin panel
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Tag)