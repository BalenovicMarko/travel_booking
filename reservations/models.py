from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class Destination(models.Model):
    naziv = models.CharField(max_length=100)
    drzava = models.CharField(max_length=100, default="Hrvatska")

    def __str__(self):
        return f"{self.naziv}, {self.drzava}"



class Accommodation(models.Model):
    TIP_SMJESTAJA = [
        ('HOTEL', 'Hotel'),
        ('APARTMAN', 'Apartman'),
        ('HOSTEL', 'Hostel'),
        ('VILA', 'Vila'),
    ]
    naziv = models.CharField(max_length=160)
    destinacija = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='smjestaji')
    tip = models.CharField(max_length=20, choices=TIP_SMJESTAJA)
    kapacitet_jedinica = models.PositiveIntegerField(default=1)
    cijena_po_nocenju = models.DecimalField(max_digits=10, decimal_places=2)
    zvjezdice = models.PositiveIntegerField(default=3)

    def __str__(self):
        return f"{self.naziv} ({self.get_tip_display()}), {self.destinacija}"



class TransportType(models.Model):
    naziv = models.CharField(max_length=50)

    def __str__(self):
        return self.naziv


class TripOffer(models.Model):
    destinacija = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='ponude_putovanja')
    datum_polaska = models.DateField()
    cijena_osnovno = models.DecimalField(max_digits=10, decimal_places=2)
    broj_mjesta = models.PositiveIntegerField(default=50)

    class Meta:
        unique_together = ('destinacija', 'datum_polaska')
        ordering = ['datum_polaska']

    def __str__(self):
        return f"{self.destinacija} – {self.datum_polaska}"


class TripTransport(models.Model):
    ponuda = models.ForeignKey(TripOffer, on_delete=models.CASCADE, related_name='prijevozi')
    transport_type = models.ForeignKey(TransportType, on_delete=models.CASCADE)
    cijena = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    max_osoba = models.PositiveIntegerField(default=50)

    def __str__(self):
        return f"{self.transport_type} – {self.ponuda} ({self.cijena} €)"


class AccommodationBooking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='smjestaj_rezervacije')
    smjestaj = models.ForeignKey(Accommodation, on_delete=models.CASCADE, related_name='accommodation_bookings')
    check_in = models.DateField()
    check_out = models.DateField()
    broj_osoba = models.PositiveIntegerField(default=1)
    ukupna_cijena = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.check_out <= self.check_in:
            raise ValidationError("Datum odjave mora biti nakon datuma prijave.")

    @property
    def nocenja(self):
        return (self.check_out - self.check_in).days

    def izracunaj_cijenu(self):
        return self.nocenja * self.smjestaj.cijena_po_nocenju * self.broj_osoba

    def save(self, *args, **kwargs):
        self.ukupna_cijena = self.izracunaj_cijenu()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user} – {self.smjestaj} ({self.check_in}–{self.check_out})"



class TripBooking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='putovanje_rezervacije')
    ponuda = models.ForeignKey(TripOffer, on_delete=models.CASCADE, related_name='trip_bookings')
    prijevoz = models.ForeignKey(TripTransport, on_delete=models.CASCADE)
    broj_osoba = models.PositiveIntegerField(default=1)
    ukupna_cijena = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def izracunaj_cijenu(self):
        return (self.ponuda.cijena_osnovno + self.prijevoz.cijena) * self.broj_osoba

    def save(self, *args, **kwargs):
        self.ukupna_cijena = self.izracunaj_cijenu()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user} – {self.ponuda} ({self.broj_osoba} osoba)"
