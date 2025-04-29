import logging

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Table, Reservation

class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = '__all__'

class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ("id", "reservation_date", "created_time", "reserved_seat_count", 'total_price', "canceled", "table")
        read_only_fields = ('total_price', "canceled", 'table')

    def validate_reserved_seat_count(self, value):
        if value < 3:
            raise ValidationError("Reservation under 4 seats is not allowed")
        if value > 10:
            raise ValidationError("Reservation over 10 seats is not allowed")
        if value % 2 != 0:
            value += 1
        return value

    def create(self, validated_data):
        seat_count = validated_data['reserved_seat_count']
        reservation_date = validated_data['reservation_date']

        available_tables = self.get_available_tables(reservation_date, seat_count)
        if not available_tables.exists():
            raise serializers.ValidationError("No available tables based on your request.")
        best_table = available_tables.order_by('seat_count').first()

        reservation = Reservation.objects.create(
            table=best_table,
            reserved_seat_count=seat_count,
            reservation_date=reservation_date,
        )
        return reservation
    def get_available_tables(self, reservation_date, seat_count):
        suitable_tables = Table.objects.filter(seat_count__gte=seat_count)
        reserved_table_ids = Reservation.objects.filter(
            reservation_date=reservation_date
        ).values_list('id', flat=True)
        available_tables = suitable_tables.exclude(id__in=reserved_table_ids)
        return available_tables
