import logging

from django.shortcuts import render
from django_filters import DateFilter
from django_filters.rest_framework import FilterSet, DjangoFilterBackend
from django_filters.rest_framework import BooleanFilter
from rest_framework.response import Response


# Create your views here.
from rest_framework import viewsets, status
from .models import Table, Reservation
from .serializers import TableSerializer, ReservationSerializer
from django.utils.timezone import now

class TableViewSet(viewsets.ModelViewSet):
    queryset = Table.objects.all()
    serializer_class = TableSerializer

class ReservationFilter(FilterSet):

    class Meta:
        model = Reservation
        fields = ["reservation_date", "canceled", "table"]


class ReservationViewSet(viewsets.ModelViewSet):
    serializer_class = ReservationSerializer
    queryset = Reservation.objects.all()
    filter_backends = [DjangoFilterBackend]
    filter_class = ReservationFilter
    filterset_fields = ["reservation_date", "canceled", "table"]
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        Reservation.objects.filter(pk=instance.pk).update(canceled=True)
        return Response(status=status.HTTP_204_NO_CONTENT)
