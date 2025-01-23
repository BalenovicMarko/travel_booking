from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse, reverse_lazy
from django.contrib.auth.views import LoginView
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Reservation, Destination, Booking, Service, Customer
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .serializers import ReservationSerializer

# RESTful API Views
class ReservationListCreateView(generics.ListCreateAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ReservationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [permissions.IsAuthenticated]


# REST API: Custom endpoint to search reservations
class ReservationSearchAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        query = request.query_params.get('q', None)
        if query:
            reservations = Reservation.objects.filter(
                Q(name__icontains=query) | Q(destination__name__icontains=query),
                user=request.user
            )
        else:
            reservations = Reservation.objects.filter(user=request.user)
        serializer = ReservationSerializer(reservations, many=True)
        return Response(serializer.data)


# Existing Views
class ReservationListView(LoginRequiredMixin, ListView):
    model = Reservation
    template_name = 'reservations/reservation_list.html'
    context_object_name = 'reservations'
    paginate_by = 10

    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user)


@login_required
def manage_reservations(request):
    reservations = Reservation.objects.filter(user=request.user)
    return render(request, 'reservations/manage_reservations.html', {
        'reservations': reservations
    })


class ReservationSearchView(LoginRequiredMixin, ListView):
    model = Reservation
    template_name = 'reservations/reservation_search.html'
    context_object_name = 'reservations'

    def get_queryset(self):
        queryset = Reservation.objects.filter(user=self.request.user)
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) | Q(destination__name__icontains=query)
            )
        return queryset


class ReservationCreateView(LoginRequiredMixin, CreateView):
    model = Reservation
    fields = ['name', 'destination', 'start_date', 'end_date']
    template_name = 'reservations/reservation_form.html'
    success_url = reverse_lazy('manage-reservations')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ReservationDetailView(LoginRequiredMixin, DetailView):
    model = Reservation
    template_name = 'reservations/reservation_detail.html'
    context_object_name = 'reservation'

    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user)


class ReservationUpdateView(LoginRequiredMixin, UpdateView):
    model = Reservation
    fields = ['name', 'destination', 'start_date', 'end_date']
    template_name = 'reservations/reservation_form.html'

    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user)

    def get_success_url(self):
        return reverse('reservation-detail', kwargs={'pk': self.object.pk})


class ReservationDeleteView(LoginRequiredMixin, DeleteView):
    model = Reservation
    template_name = 'reservations/reservation_confirm_delete.html'
    success_url = reverse_lazy('manage-reservations')

    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user)


def home(request):
    return render(request, 'reservations/home.html')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been created! You can now log in.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'reservations/register.html', {'form': form})


class CustomLoginView(LoginView):
    def get_success_url(self):
        if self.request.user.is_superuser:
            return reverse('admin:index')  
        return reverse('manage-reservations')  


def is_admin(user):
    return user.is_superuser


@login_required
def user_dashboard(request):
    return render(request, 'reservations/user_dashboard.html')


@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    return render(request, 'reservations/admin_dashboard.html')


@login_required
@user_passes_test(is_admin)
def create_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'User created successfully.')
            return redirect('admin_dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'reservations/create_user.html', {'form': form})
