import logging

import pytest
from django.utils.timezone import now, timedelta
from rest_framework.test import APIClient
from ..models import Table, Reservation

@pytest.mark.django_db
@pytest.mark.parametrize(
    "input_seat_count,expected_seat_count,seat_price,total_price",
    [
        (3, 4, 1, 4),
        (4, 4, 2, 8),
        (7, 8, 4, 32),
        (8, 8, 8, 64),
        (10, 10, 1, 9)
    ]
)
def test_reservation_makes_even_seats_and_assigns_table(test_user, input_seat_count, expected_seat_count, seat_price, total_price):
    client = APIClient()
    client.force_authenticate(user=test_user)
    table = Table.objects.create(seat_count=10, seat_price=seat_price)

    response = client.post("/reservations/", {
        "reserved_seat_count": input_seat_count,
        "reservation_date": (now() + timedelta(days=1)).date()
    }, format='json')

    assert response.status_code == 201
    data = response.json()
    assert data["reserved_seat_count"] == expected_seat_count
    assert data["total_price"] == total_price
    assert data["table"] == table.id
