"""
Module providing filter functionality for Django models.

This module provides a way to filter Django models based on certain conditions,
such as searching for specific text or selecting values from a dropdown. It
uses the `django_filters` library to implement the filtering functionality.
"""

import django_filters
from django import forms

from .models import Car


class CarFilter(django_filters.FilterSet):
    """
    A filter class for the Car model.

    This class defines the filtering options for the Car model, including
    fields to search and dropdowns to select values from. It inherits from
    the `django_filters.FilterSet` class provided by the `django_filters`
    library.
    """
    make = django_filters.CharFilter(
        lookup_expr="icontains",
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Make"}),
    )
    year = django_filters.ChoiceFilter(
        choices=Car.YEAR_IN_CHOICES,
        empty_label="Year",
        label="",
        widget=forms.Select(attrs={"class": "form-control", "placeholder": "Year"}),
    )

    class Meta:
        model = Car
        fields = ["make", "year"]
