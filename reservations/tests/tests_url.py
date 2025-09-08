from django.test import SimpleTestCase
from django.urls import reverse, resolve
from reservations import views


class TestUrls(SimpleTestCase):

    def test_home_url(self):
        url = reverse("home")
        self.assertEqual(resolve(url).func, views.home)

    def test_login_url(self):
        url = reverse("login")
        self.assertEqual(resolve(url).func.view_class, views.CustomLoginView)

    def test_register_url(self):
        url = reverse("register")
        self.assertEqual(resolve(url).func, views.register)

    def test_book_accommodation_url(self):
        url = reverse("book-accommodation")
        self.assertEqual(resolve(url).func.view_class, views.AccommodationBookingCreateView)

    def test_book_trip_url(self):
        url = reverse("book-trip")
        self.assertEqual(resolve(url).func.view_class, views.TripBookingCreateView)

    def test_update_accommodation_booking_url(self):
        url = reverse("update-accommodation-booking", args=[1])
        self.assertEqual(resolve(url).func.view_class, views.AccommodationBookingUpdateView)

    def test_update_trip_booking_url(self):
        url = reverse("update-trip-booking", args=[1])
        self.assertEqual(resolve(url).func.view_class, views.TripBookingUpdateView)

    def test_search_url(self):
        url = reverse("search")
        self.assertEqual(resolve(url).func.view_class, views.SearchView)
