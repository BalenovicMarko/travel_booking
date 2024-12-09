from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse
from django.contrib.auth.views import LoginView


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
        # Provjera je li korisnik superuser
        if self.request.user.is_superuser:
            return '/admin/'  # Preusmjeri na admin stranicu
        else:
            return '/dashboard/user/'  # Preusmjeri na korisnički dashboard

def is_admin(user):
    return user.userprofile.is_admin

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
            UserProfile.objects.create(user=user, is_admin=request.POST.get('is_admin', False))
            messages.success(request, 'User created successfully.')
            return redirect('admin_dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'reservations/create_user.html', {'form': form})
