from django.db import models

# Create your models here.
class Customer(models.Model):
    name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    email = models.EmailField(max_length=200, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    # For Laravel, this is added in migrations file
    # And the model, only includes the connection of foreign key and sql statement

    # str is for user friendly representation of the object
    def __str__(self) -> str:
        return self.name

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
        return self.name


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

    def __str__(self) -> str:
        return self.product.name + " ordered by " + self.customer.name

class Tag(models.Model):

    name = models.CharField(max_length=200, unique=True, null=True)

    def __str__(self) -> str:
        return self.name
    