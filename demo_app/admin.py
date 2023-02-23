"""
This module registers models with the Django admin site.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Car
from .models import User
from .models import BuyersRequest

admin.site.register(Car)
admin.site.register(User, UserAdmin)
admin.site.register(BuyersRequest)
