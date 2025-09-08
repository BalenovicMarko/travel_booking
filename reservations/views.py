from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
import json
from django.urls import reverse_lazy
from .models import Accommodation, TripOffer, AccommodationBooking, TripBooking
from .forms import (
    AccommodationForm, TripOfferForm,
    AccommodationBookingForm, TripBookingForm,
    AccommodationBookingUpdateForm, TripBookingUpdateForm,
)



def home(request):
    return render(request, 'reservations/home.html')


def register(request):
    """Registracija korisnika"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Račun je uspješno kreiran! Možete se prijaviti.')
            return redirect('login')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    label = form.fields[field].label if field != '__all__' else ''
                    messages.error(request, f"❌ {label} {error}".strip())
    else:
        form = UserCreationForm()
    return render(request, 'reservations/register.html', {'form': form})



class CustomLoginView(LoginView):
    template_name = 'reservations/login.html'
    def get_success_url(self):
        return reverse_lazy('home')


@login_required
def user_dashboard(request):
    return render(request, 'reservations/user_dashboard.html')


@login_required
@user_passes_test(lambda u: u.is_superuser)
def admin_dashboard(request):
    return render(request, 'reservations/admin_dashboard.html')



class SuperuserRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser


def show_form_errors(request, form):
    """Prikazuje sve greške iz forme samo jednom, bez duplikata"""
    seen = set()
    for field, errors in form.errors.items():
        for error in errors:
            msg = f"❌ {form.fields[field].label}: {error}" if field != '__all__' else f"❌ {error}"
            if msg not in seen:
                messages.error(request, msg)
                seen.add(msg)



class AccommodationListView(LoginRequiredMixin, SuperuserRequiredMixin, ListView):
    model = Accommodation
    template_name = 'reservations/accommodation_list.html'
    context_object_name = 'smjestaji'


class AccommodationCreateView(LoginRequiredMixin, SuperuserRequiredMixin, CreateView):
    model = Accommodation
    form_class = AccommodationForm
    template_name = 'reservations/accommodation_form.html'
    success_url = reverse_lazy('accommodation-list')

    def form_invalid(self, form):
        show_form_errors(self.request, form)
        return super().form_invalid(form)


class AccommodationUpdateView(LoginRequiredMixin, SuperuserRequiredMixin, UpdateView):
    model = Accommodation
    form_class = AccommodationForm
    template_name = 'reservations/accommodation_form.html'
    success_url = reverse_lazy('accommodation-list')

    def form_invalid(self, form):
        show_form_errors(self.request, form)
        return super().form_invalid(form)


class AccommodationDeleteView(LoginRequiredMixin, SuperuserRequiredMixin, DeleteView):
    model = Accommodation
    template_name = 'reservations/confirm_delete.html'
    success_url = reverse_lazy('accommodation-list')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['back_url'] = reverse_lazy('accommodation-list')
        ctx['naslov'] = 'Brisanje smještaja'
        return ctx



class TripOfferListView(LoginRequiredMixin, SuperuserRequiredMixin, ListView):
    model = TripOffer
    template_name = 'reservations/offer_list.html'
    context_object_name = 'ponude'


class TripOfferCreateView(LoginRequiredMixin, SuperuserRequiredMixin, CreateView):
    model = TripOffer
    form_class = TripOfferForm
    template_name = 'reservations/offer_form.html'
    success_url = reverse_lazy('offer-list')

    def form_invalid(self, form):
        show_form_errors(self.request, form)
        return super().form_invalid(form)


class TripOfferUpdateView(LoginRequiredMixin, SuperuserRequiredMixin, UpdateView):
    model = TripOffer
    form_class = TripOfferForm
    template_name = 'reservations/offer_form.html'
    success_url = reverse_lazy('offer-list')

    def form_invalid(self, form):
        show_form_errors(self.request, form)
        return super().form_invalid(form)


class TripOfferDeleteView(LoginRequiredMixin, SuperuserRequiredMixin, DeleteView):
    model = TripOffer
    template_name = 'reservations/confirm_delete.html'
    success_url = reverse_lazy('offer-list')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['back_url'] = reverse_lazy('offer-list')
        ctx['naslov'] = 'Brisanje ponude putovanja'
        return ctx


class MojeRezervacijeView(LoginRequiredMixin, ListView):
    template_name = 'reservations/my_bookings.html'
    context_object_name = 'rezultati'

    def get_queryset(self):
        return []

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['smjestaji'] = AccommodationBooking.objects.filter(user=self.request.user).order_by('-created_at')
        ctx['putovanja'] = TripBooking.objects.filter(user=self.request.user).order_by('-created_at')
        return ctx


class AccommodationBookingCreateView(LoginRequiredMixin, CreateView):
    model = AccommodationBooking
    form_class = AccommodationBookingForm
    template_name = 'reservations/booking_accommodation_form.html'
    success_url = reverse_lazy('moje-rezervacije')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def form_invalid(self, form):
        show_form_errors(self.request, form)
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        smjestaji = Accommodation.objects.all()
        ctx['smjestaji'] = [{
            'id': s.id,
            'naziv': s.naziv,
            'destinacija_id': s.destinacija.id if s.destinacija else None,
            'tip': s.get_tip_display(),
            'cijena_po_nocenju': float(s.cijena_po_nocenju),
            'zvjezdice': s.zvjezdice,
        } for s in smjestaji]
        return ctx


class AccommodationBookingUpdateView(LoginRequiredMixin, UpdateView):
    model = AccommodationBooking
    form_class = AccommodationBookingUpdateForm
    template_name = 'reservations/booking_accommodation_update.html'
    success_url = reverse_lazy('moje-rezervacije')

    def get_queryset(self):
        return AccommodationBooking.objects.filter(user=self.request.user)

    def form_valid(self, form):
        booking = form.save(commit=False)
        booking.ukupna_cijena = booking.izracunaj_cijenu()
        booking.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        show_form_errors(self.request, form)
        return super().form_invalid(form)


class AccommodationBookingDeleteView(LoginRequiredMixin, DeleteView):
    model = AccommodationBooking
    template_name = 'reservations/confirm_delete.html'
    success_url = reverse_lazy('moje-rezervacije')

    def get_queryset(self):
        return AccommodationBooking.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['back_url'] = reverse_lazy('moje-rezervacije')
        ctx['naslov'] = 'Brisanje rezervacije smještaja'
        return ctx


class AccommodationBookingDetailView(LoginRequiredMixin, DetailView):
    model = AccommodationBooking
    template_name = 'reservations/booking_accommodation_detail.html'
    context_object_name = 'rezervacija'

    def get_queryset(self):
        return AccommodationBooking.objects.filter(user=self.request.user)


class TripBookingCreateView(LoginRequiredMixin, CreateView):
    model = TripBooking
    form_class = TripBookingForm
    template_name = 'reservations/booking_trip_form.html'
    success_url = reverse_lazy('moje-rezervacije')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def form_invalid(self, form):
        show_form_errors(self.request, form)
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ponude = TripOffer.objects.prefetch_related('prijevozi__transport_type')
        ponude_list = []
        for p in ponude:
            vozila_list = [{
                'id': t.id,
                'tip': t.transport_type.naziv,
                'cijena': float(t.cijena)
            } for t in p.prijevozi.all()]
            ponude_list.append({
                'id': p.id,
                'destinacija': str(p.destinacija),
                'datum_polaska': p.datum_polaska.strftime('%d.%m.%Y'),
                'cijena_osnovno': float(p.cijena_osnovno),
                'vozila': vozila_list
            })
        ctx['ponude_json'] = json.dumps(ponude_list)
        return ctx


class TripBookingUpdateView(LoginRequiredMixin, UpdateView):
    model = TripBooking
    form_class = TripBookingUpdateForm
    template_name = 'reservations/booking_trip_update.html'
    success_url = reverse_lazy('moje-rezervacije')

    def get_queryset(self):
        return TripBooking.objects.filter(user=self.request.user)

    def form_valid(self, form):
        booking = form.save(commit=False)
        booking.ukupna_cijena = booking.izracunaj_cijenu()
        booking.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        show_form_errors(self.request, form)
        return super().form_invalid(form)


class TripBookingDeleteView(LoginRequiredMixin, DeleteView):
    model = TripBooking
    template_name = 'reservations/confirm_delete.html'
    success_url = reverse_lazy('moje-rezervacije')

    def get_queryset(self):
        return TripBooking.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['back_url'] = reverse_lazy('moje-rezervacije')
        ctx['naslov'] = 'Brisanje rezervacije putovanja'
        return ctx


class TripBookingDetailView(LoginRequiredMixin, DetailView):
    model = TripBooking
    template_name = 'reservations/booking_trip_detail.html'
    context_object_name = 'rezervacija'

    def get_queryset(self):
        return TripBooking.objects.filter(user=self.request.user)



class SearchView(LoginRequiredMixin, ListView):
    template_name = 'reservations/search.html'
    context_object_name = 'rezultati'

    def get_queryset(self):
        return []

    def get_context_data(self, **kwargs):
        q = self.request.GET.get('q', '').strip()
        ctx = super().get_context_data(**kwargs)

        smj_qs = AccommodationBooking.objects.filter(user=self.request.user)
        put_qs = TripBooking.objects.filter(user=self.request.user)

        if q:
            smj_qs = smj_qs.filter(
                Q(smjestaj__naziv__icontains=q) |
                Q(smjestaj__destinacija__naziv__icontains=q)
            )
            put_qs = put_qs.filter(
                Q(ponuda__destinacija__naziv__icontains=q)
            )

        ctx['query'] = q
        ctx['smjestaji'] = smj_qs.order_by('-created_at')
        ctx['putovanja'] = put_qs.order_by('-created_at')
        return ctx
