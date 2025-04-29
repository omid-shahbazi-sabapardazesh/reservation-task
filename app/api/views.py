from django.db import transaction
from django_filters.rest_framework import FilterSet, DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.views import APIView

from .models import Table, Reservation
from .serializers import TableSerializer, ReservationSerializer

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
    permission_classes = [IsAuthenticated]
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        Reservation.objects.filter(pk=instance.pk).update(canceled=True)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['post'], url_path='cancel')
    def cancel_reservation(self, request, pk=None):
        with transaction.atomic():
            reservation = Reservation.objects.select_for_update().get(pk=pk)

            if reservation.user != request.user or not request.user.is_owner:
                return Response({'detail': 'Not allowed to cancel this reservation.'},
                                status=status.HTTP_403_FORBIDDEN)

            reservation.is_cancelled = True
            reservation.save()

            return Response({'status': 'Reservation cancelled'}, status=status.HTTP_200_OK)
