# Create your views here.
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import update_last_login
from django.contrib.auth.signals import user_logged_in
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.shortcuts import render, redirect
from django.utils import timezone
from django.core.cache import cache
from .forms import CustomAuthenticationForm, SignUpForm
from django.contrib.auth import logout

MAX_ATTEMPTS = 5
LOCKOUT_TIME = 5 * 60  # 5 minutes in seconds


def custom_logout(request):
    logout(request)
    messages.success(request, "You have successfully logged out.")
    return redirect('login')  # Redirect to the login page after logout

def custom_login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')  # Use 'username' to get email input
            password = form.cleaned_data.get('password')
            
            # Ensure the email is checked for lockout
            lockout_time = cache.get(f'lockout_time_{email}')
            if lockout_time and timezone.now() < lockout_time:
                messages.error(request, 'Your account is locked. Please try again later.')
                return render(request, 'core/login.html', {'form': form})
            print(f"Email: {email}, Password: {password}")

            user = authenticate(request, email=email, password=password)
            if user is not None:
                # Reset failed attempts on successful login
                cache.delete(f'failed_attempts_{email}')
                cache.delete(f'lockout_time_{email}')

                login(request, user)
                messages.success(request, f"Welcome back, {user.username}!")
                return redirect('home')
            else:
                # Handle failed attempts
                failed_attempts = cache.get(f'failed_attempts_{email}', 0) + 1
                cache.set(f'failed_attempts_{email}', failed_attempts, LOCKOUT_TIME)

                if failed_attempts >= MAX_ATTEMPTS:
                    lockout_time = timezone.now() + timezone.timedelta(seconds=LOCKOUT_TIME)
                    cache.set(f'lockout_time_{email}', lockout_time, LOCKOUT_TIME)
                    messages.error(request, 'Account locked due to too many failed attempts. Try again in 5 minutes.')
                else:
                    messages.error(request, 'Invalid email or password.')
        else:
            messages.error(request, 'Invalid email or password.')
    else:
        form = CustomAuthenticationForm()

    return render(request, 'core/login.html', {'form': form})










def custom_logout(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('login')  # Redirect to login page after logging out





def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user=form.save()
            login(request, user)
            messages.success(request, 'Account created successfully')
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'core/signup.html', {'form': form})




# core/views.py


def home(request):
    
    return render(request, 'core/home.html')




# Create your views here.
