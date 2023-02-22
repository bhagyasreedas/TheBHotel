import django_filters
from .models import *
class PriceFilter(django_filters.FilterSet):
    class Meta:
        model = Hotel
        fields = {
            'price':['lt','gt']
            }
