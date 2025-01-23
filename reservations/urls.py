from django.urls import path
from .views import (
    ReservationCreateView, ReservationListView, ReservationDetailView,
    ReservationUpdateView, ReservationDeleteView, home, register,
    CustomLoginView, user_dashboard, admin_dashboard, create_user,
    manage_reservations, ReservationSearchView, ReservationListCreateView, ReservationDetailView
)
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', home, name='home'),
    path('reservations/', ReservationListView.as_view(), name='reservation-list'),
    path('reservations/create/', ReservationCreateView.as_view(), name='reservation-create'),
    path('reservations/manage/', manage_reservations, name='manage-reservations'),
    path('reservations/search/', ReservationSearchView.as_view(), name='reservation-search'),
    path('reservations/<int:pk>/', ReservationDetailView.as_view(), name='reservation-detail'),
    path('reservations/<int:pk>/update/', ReservationUpdateView.as_view(), name='reservation-update'),
    path('reservations/<int:pk>/delete/', ReservationDeleteView.as_view(), name='reservation-delete'),
    path('api/reservations/', ReservationListCreateView.as_view(), name='api-reservation-list'),
    path('api/reservations/<int:pk>/', ReservationDetailView.as_view(), name='api-reservation-detail'),
    path('login/', CustomLoginView.as_view(template_name='reservations/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('register/', register, name='register'),
    path('dashboard/user/', user_dashboard, name='user_dashboard'),
    path('dashboard/admin/', admin_dashboard, name='admin_dashboard'),
    path('create_user/', create_user, name='create_user'),
]
