import uuid
import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models

from djmoney.models.fields import MoneyField
from djmoney.models.validators import MaxMoneyValidator
from djmoney.models.validators import MinMoneyValidator


class Car(models.Model):
    """
    Car related information - model class
    """

    CONDITION_CHOICE = (
        ("POOR", "Poor"),
        ("FAIR", "Fair"),
        ("GOOD", "Good"),
        ("EXCELLENT", "Excellent"),
    )

    today = datetime.datetime.now()
    current_year = today.year

    YEAR_IN_CHOICES = [(str(x), str(x)) for x in range(2000, current_year + 1)]
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    make = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    year = models.CharField(
        max_length=4,
        choices=YEAR_IN_CHOICES,
        default=YEAR_IN_CHOICES[0][0],
    )
    seller_name = models.CharField(max_length=255)
    seller_mobile = models.CharField(max_length=16)

    condition = models.CharField(
        max_length=9,
        choices=CONDITION_CHOICE,
        default=CONDITION_CHOICE[2][0],
    )
    price = MoneyField(
        max_digits=6,
        decimal_places=0,
        default_currency="USD",
        validators=[
            MinMoneyValidator(1000),
            MaxMoneyValidator(100000),
        ],
    )

    is_sold = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.make} {self.model}"


class User(AbstractUser):
    """
    Custom user class
    """

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class BuyersRequest(models.Model):
    """
    Buyer's request specific details
    """

    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    buyer_name = models.CharField(max_length=255)
    buyer_mobile = models.CharField(max_length=16)
    car = models.ForeignKey(Car, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.buyer_name}"
