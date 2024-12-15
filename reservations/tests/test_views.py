from django.test import TestCase
from django.urls import reverse
from reservations.models import Reservation
from datetime import date

class ReservationViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.reservation1 = Reservation.objects.create(name="Rezervacija 1", date=date(2024, 12, 15))
        cls.reservation2 = Reservation.objects.create(name="Rezervacija 2", date=date(2024, 12, 16))

    def test_reservation_list_view(self):
        response = self.client.get(reverse('reservation-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Rezervacija 1")
        self.assertContains(response, "Rezervacija 2")

    def test_reservation_detail_view(self):
        response = self.client.get(reverse('reservation-detail', args=[self.reservation1.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Rezervacija 1")
        self.assertContains(response, "Dec. 15, 2024")  

