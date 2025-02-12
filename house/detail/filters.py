from django_filters import FilterSet
from .models import OwnerApartment


class OwnerApartmentFilter(FilterSet):
    class Meta:
        model = OwnerApartment
        fields = {
            'address': ['exact'],
            'price': ['gt', 'lt'],

        }




