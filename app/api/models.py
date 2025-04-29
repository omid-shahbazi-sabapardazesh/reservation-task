from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from rest_framework.exceptions import ValidationError

from core import settings


# Create your models here.


def validate_even(value):
    if value % 2 != 0:
        raise ValidationError(f"Must be an even number")

class Table(models.Model):
    id = models.AutoField(primary_key=True)
    seat_count = models.PositiveIntegerField(default=10, validators=[MinValueValidator(4), MaxValueValidator(10), validate_even])
    seat_price = models.PositiveIntegerField()


class Reservation(models.Model):
    id = models.AutoField(primary_key=True)
    reservation_date = models.DateField()
    created_time  = models.DateTimeField(auto_now_add=True)
    reserved_seat_count = models.PositiveIntegerField(validators=[MaxValueValidator(10)])
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    canceled = models.BooleanField(default=False)
    total_price = models.PositiveIntegerField()

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reservations'
    )
    def save(self, *args, **kwargs):
        if self.reserved_seat_count == self.table.seat_count:
            self.total_price = self.table.seat_price * (self.reserved_seat_count - 1)
        else:
            self.total_price = self.table.seat_price * self.reserved_seat_count
        super().save(*args, **kwargs)
