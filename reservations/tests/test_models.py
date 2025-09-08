from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from datetime import date, timedelta
from reservations.models import (
    Destination, Accommodation, TransportType,
    TripOffer, TripTransport,
    AccommodationBooking, TripBooking
)


class DestinationModelTest(TestCase):
    def test_str_representation(self):
        d = Destination.objects.create(naziv="Zagreb", drzava="Hrvatska")
        self.assertEqual(str(d), "Zagreb, Hrvatska")

class AccommodationModelTest(TestCase):
    def setUp(self):
        self.dest = Destination.objects.create(naziv="Split")

    def test_str_representation(self):
        a = Accommodation.objects.create(
            naziv="Hotel Adriatic",
            destinacija=self.dest,
            tip="HOTEL",
            kapacitet_jedinica=2,
            cijena_po_nocenju=50,
            zvjezdice=4
        )
        self.assertIn("Hotel Adriatic", str(a))
        self.assertIn("Hotel", str(a))
        self.assertIn("Split", str(a))


class TransportTypeModelTest(TestCase):
    def test_str_representation(self):
        t = TransportType.objects.create(naziv="Autobus")
        self.assertEqual(str(t), "Autobus")


class TripOfferModelTest(TestCase):
    def setUp(self):
        self.dest = Destination.objects.create(naziv="Dubrovnik")

    def test_str_representation(self):
        o = TripOffer.objects.create(
            destinacija=self.dest,
            datum_polaska=date.today() + timedelta(days=5),
            cijena_osnovno=200,
        )
        self.assertIn("Dubrovnik", str(o))
        self.assertIn(str(o.datum_polaska), str(o))


class TripTransportModelTest(TestCase):
    def setUp(self):
        self.dest = Destination.objects.create(naziv="Rovinj")
        self.offer = TripOffer.objects.create(
            destinacija=self.dest,
            datum_polaska=date.today() + timedelta(days=10),
            cijena_osnovno=300
        )
        self.bus = TransportType.objects.create(naziv="Bus")

    def test_str_representation(self):
        t = TripTransport.objects.create(
            ponuda=self.offer,
            transport_type=self.bus,
            cijena=50,
            max_osoba=40
        )
        self.assertIn("Bus", str(t))
        self.assertIn("Rovinj", str(t))


class AccommodationBookingModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser")
        self.dest = Destination.objects.create(naziv="Zadar")
        self.smjestaj = Accommodation.objects.create(
            naziv="Villa Sun",
            destinacija=self.dest,
            tip="VILA",
            kapacitet_jedinica=4,
            cijena_po_nocenju=80,
            zvjezdice=5
        )

    def test_price_calculation(self):
        booking = AccommodationBooking.objects.create(
            user=self.user,
            smjestaj=self.smjestaj,
            check_in=date.today(),
            check_out=date.today() + timedelta(days=3),
            broj_osoba=2
        )
        expected_price = 3 * 80 * 2
        self.assertEqual(booking.ukupna_cijena, expected_price)


class TripBookingModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser2")
        self.dest = Destination.objects.create(naziv="Makarska")
        self.offer = TripOffer.objects.create(
            destinacija=self.dest,
            datum_polaska=date.today() + timedelta(days=7),
            cijena_osnovno=150
        )
        self.bus = TransportType.objects.create(naziv="Autobus")
        self.transport = TripTransport.objects.create(
            ponuda=self.offer,
            transport_type=self.bus,
            cijena=50,
            max_osoba=3
        )

    def test_price_calculation(self):
        booking = TripBooking.objects.create(
            user=self.user,
            ponuda=self.offer,
            prijevoz=self.transport,
            broj_osoba=2
        )
        expected_price = (150 + 50) * 2
        self.assertEqual(booking.ukupna_cijena, expected_price)
