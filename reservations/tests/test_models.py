from django.test import TestCase
from reservations.models import Reservation
from datetime import date

class ReservationModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):   
        Reservation.objects.create(name="Rezervacija 1", date=date(2024, 12, 15))
        Reservation.objects.create(name="Rezervacija 2", date=date(2024, 12, 16))

    def test_reservation_creation(self):
        reservation = Reservation.objects.get(name="Rezervacija 1")
        self.assertEqual(reservation.date, date(2024, 12, 15))
        self.assertEqual(reservation.name, "Rezervacija 1")

    def test_reservation_count(self):
        self.assertEqual(Reservation.objects.count(), 2)
