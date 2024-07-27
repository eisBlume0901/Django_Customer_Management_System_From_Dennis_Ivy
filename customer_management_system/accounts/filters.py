import django_filters
from django_filters import DateFilter, CharFilter
from .models import * # Using models for django_filters

class OrderFilter(django_filters.FilterSet):
    # Allows searching for a customer by name
    product_name = CharFilter(field_name='product__name', lookup_expr='icontains')

    # Allows date range filtering
    start_date = DateFilter(field_name='date_created', lookup_expr='gte')
    end_date = DateFilter(field_name='date_created', lookup_expr='lte')

    class Meta:
        model = Order
        fields = '__all__'
        exclude = ['product', 'customer', 'date_created']
