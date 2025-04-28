from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

# Create your models here.

class Table(models.Model):
    id = models.AutoField(primary_key=True)
    seat_count = models.PositiveIntegerField(default=10, validators=[MinValueValidator(4), MaxValueValidator(10)])
    seat_price = models.PositiveIntegerField()


class Reservation(models.Model):
    id = models.AutoField(primary_key=True)
    reservation_date = models.DateField()
    created_time  = models.DateTimeField(auto_now_add=True)
    reserved_seat_count = models.PositiveIntegerField(validators=[MinValueValidator(4), MaxValueValidator(10)])
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    canceled = models.BooleanField(default=False)

