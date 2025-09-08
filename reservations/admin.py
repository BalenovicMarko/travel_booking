from django.contrib import admin
from .models import Destination, Accommodation, TripOffer, TripTransport, TransportType, AccommodationBooking, TripBooking


@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ('naziv', 'drzava')


@admin.register(Accommodation)
class AccommodationAdmin(admin.ModelAdmin):
    list_display = ('naziv', 'destinacija', 'tip', 'kapacitet_jedinica', 'cijena_po_nocenju')
    list_filter = ('tip', 'destinacija')
    search_fields = ('naziv',)


@admin.register(TransportType)
class TransportTypeAdmin(admin.ModelAdmin):
    list_display = ('naziv',)


class TripTransportInline(admin.TabularInline):
    model = TripTransport
    extra = 1

@admin.register(TripOffer)
class TripOfferAdmin(admin.ModelAdmin):
    list_display = ('destinacija', 'datum_polaska', 'cijena_osnovno', 'broj_mjesta')
    inlines = [TripTransportInline]
    list_filter = ('destinacija', 'datum_polaska')
    search_fields = ('destinacija__naziv',)


@admin.register(AccommodationBooking)
class AccommodationBookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'smjestaj', 'check_in', 'check_out', 'broj_osoba', 'ukupna_cijena')
    list_filter = ('smjestaj',)
    search_fields = ('user__username', 'smjestaj__naziv')


@admin.register(TripBooking)
class TripBookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'ponuda', 'prijevoz', 'broj_osoba', 'ukupna_cijena')
    list_filter = ('ponuda__destinacija', 'prijevoz')
    search_fields = ('user__username', 'ponuda__destinacija__naziv')
