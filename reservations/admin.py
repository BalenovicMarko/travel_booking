from django.contrib import admin
from .models import Destination, Booking, Customer, Service

admin.site.register(Destination)
admin.site.register(Booking)
admin.site.register(Customer)
admin.site.register(Service)