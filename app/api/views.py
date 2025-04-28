from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView


# Create your views here.
from rest_framework import viewsets, status
from .models import Table, Reservation
from .serializers import TableSerializer, ReservationSerializer
from django.utils.timezone import now

class TableViewSet(viewsets.ModelViewSet):
    queryset = Table.objects.all()
    serializer_class = TableSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        Table.objects.filter(pk=instance.pk).update(canceled=True)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ReservationViewSet(viewsets.ModelViewSet):
    serializer_class = ReservationSerializer

    def get_queryset(self):
        # TODO django-filter???????
        if self.action == 'list':
            today = now().date()
            return Reservation.objects.filter(date__gte=today)
        return super().get_queryset()
