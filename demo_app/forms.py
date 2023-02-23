"""
This module contains form classes related to Car and BuyersRequest models.
"""
from django import forms

from .models import Car
from .models import BuyersRequest


class ListCarForm(forms.ModelForm):
    """
    Form class for creating and updating a Car object. The form excludes the 
    `is_sold` field.
    """
    class Meta:
        model = Car
        exclude = ("is_sold",)


class BuyersRequestForm(forms.ModelForm):
    """
    Form class for creating and updating a BuyersRequest object. The form 
    excludes the `car` field.
    """
    class Meta:
        model = BuyersRequest
        exclude = ("car",)
