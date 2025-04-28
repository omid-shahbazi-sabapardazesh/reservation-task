from django.shortcuts import render
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
    future_only = BooleanFilter(method='filter_future_only')

    class Meta:
        model = Reservation
        fields = ['future_only']

    def filter_future_only(self, queryset, name, value):
        if value:
            return queryset.filter(reservation_date__gte=now()).order_by('reservation_date')

class ReservationViewSet(viewsets.ModelViewSet):
    serializer_class = ReservationSerializer
    queryset = Reservation.objects.all()
    filter_backends = [DjangoFilterBackend]
    filter_class = ReservationFilter

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        Reservation.objects.filter(pk=instance.pk).update(canceled=True)
        return Response(status=status.HTTP_204_NO_CONTENT)
