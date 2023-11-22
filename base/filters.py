from django_filters.rest_framework import FilterSet
from .models import *

class ProductFilter(FilterSet):
    class Meta:
        model = Product
        fields = {
            'catagory_id':['exact'],
            'price': ['gt','lt']
        }