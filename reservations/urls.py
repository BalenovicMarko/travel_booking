from django.urls import path
from django.contrib.auth import views as auth_views
from reservations.views import CustomLoginView, register, user_dashboard, admin_dashboard

urlpatterns = [
    path('login/', CustomLoginView.as_view(template_name='reservations/login.html'), name='login'),
    path('register/', register, name='register'),  # Dodano za registraciju
    path('dashboard/user/', user_dashboard, name='user_dashboard'),
    path('dashboard/admin/', admin_dashboard, name='admin_dashboard'),
    path('logout/', auth_views.LogoutView.as_view(template_name='reservations/logout.html'), name='logout'),
]
