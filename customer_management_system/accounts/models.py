from django.db import models
from django.contrib.auth.models import User, Group


# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE) # CASCADE means that if the user is deleted, the customer will also be deleted
    name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    email = models.EmailField(max_length=200, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    # For Laravel, this is added in migrations file
    # And the model, only includes the connection of foreign key and sql statement

    # str is for user friendly representation of the object

    # Overriding the save method to add the user to the customer group so that we can easily manage permissions
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        group, created = Group.objects.get_or_create(name='customer')
        self.user.groups.add(group)
    def __str__(self) -> str:
        return self.name if self.name else "Unknown Customer"

class Product(models.Model):
    CATEGORY = (
        ('Indoor', 'Indoor'),
        ('Outdoor', 'Outdoor'),
    )
    name = models.CharField(max_length=200, null=True)
    price = models.FloatField(null=True)
    # choices gives you a default dropdown
    category = models.CharField(max_length=200, null=True, choices=CATEGORY)
    description = models.TextField(null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    tags = models.ManyToManyField('Tag')


    def __str__(self) -> str:
        return self.name if self.name else "Unknown Product"


class Order(models.Model):
    # Enums but Tuples in Django
    STATUS = (
        ('Pending', 'Pending'),
        ('Out for delivery', 'Out for delivery'),
        ('Delivered', 'Delivered'),
    )

    # Establishing relationship with Customer and Product using foreign key and on_delete
    # on_delete means if the customer is deleted, the order wil not be deleted
    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    # date_updated = models.DateTimeField(auto_now=True, null=True) next time add this
    status = models.CharField(max_length=200, null=True, choices=STATUS)


    # Resolved the issue of NoneType object has no attribute name
    def __str__(self) -> str:
        product_name = self.product.name if self.product else "Unknown Product"
        customer_name = self.customer.name if self.customer else "Unknown Customer"
        return f"{product_name} ordered by {customer_name}"
class Tag(models.Model):

    name = models.CharField(max_length=200, unique=True, null=True)

    def __str__(self) -> str:
        return self.name
    