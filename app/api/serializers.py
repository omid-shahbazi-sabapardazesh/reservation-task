from rest_framework import serializers
from .models import Table, Reservation

class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = '__all__'

class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ("id", "reservation_date", "created_time", "reserved_seat_count", "table", "canceled")
        read_only_fields = ('total_price',)

    def validate_reserved_seat_count(self, value):
        if value % 2 != 0:
            value += 1
        return value