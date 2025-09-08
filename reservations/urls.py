from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (
    home, register, CustomLoginView,
    user_dashboard, admin_dashboard,
    MojeRezervacijeView, SearchView,
    AccommodationBookingCreateView, TripBookingCreateView,
    AccommodationBookingUpdateView, TripBookingUpdateView,
    AccommodationBookingDeleteView, TripBookingDeleteView,
    AccommodationBookingDetailView, TripBookingDetailView,
)

urlpatterns = [
    
    path('', home, name='home'),
    path('login/', CustomLoginView.as_view(template_name='reservations/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('register/', register, name='register'),

    
    path('dashboard/', user_dashboard, name='user-dashboard'),
    path('admin-dashboard/', admin_dashboard, name='admin-dashboard'),

    
    path('rezervacije/moje/', MojeRezervacijeView.as_view(), name='moje-rezervacije'),

    
    path('rezerviraj/smjestaj/', AccommodationBookingCreateView.as_view(), name='book-accommodation'),
    path('rezerviraj/putovanje/', TripBookingCreateView.as_view(), name='book-trip'),

    
    path('rezervacije/smjestaj/<int:pk>/', AccommodationBookingDetailView.as_view(), name='detail-accommodation-booking'),
    path('rezervacije/putovanje/<int:pk>/', TripBookingDetailView.as_view(), name='detail-trip-booking'),

    
    path('rezervacije/smjestaj/<int:pk>/obrisi/', AccommodationBookingDeleteView.as_view(), name='delete-accommodation-booking'),
    path('rezervacije/putovanje/<int:pk>/obrisi/', TripBookingDeleteView.as_view(), name='delete-trip-booking'),

   
    path('rezervacije/smjestaj/<int:pk>/uredi/', AccommodationBookingUpdateView.as_view(), name='update-accommodation-booking'),
    path('rezervacije/putovanje/<int:pk>/uredi/', TripBookingUpdateView.as_view(), name='update-trip-booking'),

    
    path('pretraga/', SearchView.as_view(), name='search'),
]

