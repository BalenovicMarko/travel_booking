from django.urls import path
from django.contrib.auth import views as auth_views
from reservations.views import CustomLoginView, register, user_dashboard, admin_dashboard
from . import views

urlpatterns = [
    path('', views.home, name='home'),  
    path('login/', views.CustomLoginView.as_view(template_name='reservations/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('register/', views.register, name='register'),  
    path('dashboard/user/', views.user_dashboard, name='user_dashboard'),
    path('dashboard/admin/', views.admin_dashboard, name='admin_dashboard'),
]
