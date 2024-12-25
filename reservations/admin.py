from django.contrib import admin
from .models import Destination, Booking, Service, Customer, UserProfile, Reservation

admin.site.register(Destination)
admin.site.register(Booking)
admin.site.register(Service)
admin.site.register(Customer)
admin.site.register(UserProfile)
admin.site.register(Reservation)
