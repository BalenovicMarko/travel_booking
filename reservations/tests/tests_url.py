from django.test import SimpleTestCase
from django.urls import reverse, resolve
from reservations.views import ReservationListView, ReservationDetailView

class TestUrls(SimpleTestCase):

    def test_reservation_list_url_resolves(self):
        url = reverse('reservation-list')  
        self.assertEqual(resolve(url).func.view_class, ReservationListView)

    def test_reservation_detail_url_resolves(self):
        url = reverse('reservation-detail', args=[1])  
        self.assertEqual(resolve(url).func.view_class, ReservationDetailView)


    def test_invalid_url_returns_404(self):
        response = self.client.get('/nonexistent-url/')
        self.assertEqual(response.status_code, 404)
