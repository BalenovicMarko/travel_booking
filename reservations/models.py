from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError



class Destination(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    country = models.CharField(max_length=50)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


class Booking(models.Model):
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name="bookings")
    customer_name = models.CharField(max_length=100)
    check_in = models.DateField()
    check_out = models.DateField()

    @property
    def total_price(self):
        days = (self.check_out - self.check_in).days
        return days * self.destination.price_per_night

    def clean(self):
        if self.check_out <= self.check_in:
            raise ValidationError("Check-out date must be after check-in date.")

    def __str__(self):
        return f"{self.customer_name} - {self.destination.name}"



class Service(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name



class Customer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    address = models.TextField()

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)



from django.utils.dateformat import DateFormat

class Reservation(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reservations", null=True, blank=True)
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name="reservations", null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    def __str__(self):
        
        formatted_date = DateFormat(self.date).format('d.m.Y') if self.date else "nema datuma"
        return f"{self.name} - {formatted_date}"