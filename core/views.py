# Create your views here.
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import render, redirect
from django.utils import timezone
from django.core.cache import cache
from .forms import CustomAuthenticationForm, SignUpForm
from django.contrib.auth import logout
from django.conf import settings
import datetime

def custom_login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        email = request.POST.get('email')

        lockout_time = cache.get(f'lockout_time_{email}')
        if lockout_time and timezone.now() < lockout_time:
            remaining_time = int((lockout_time - timezone.now()).total_seconds())
            messages.error(request, f'Your account is locked. Please try again in {remaining_time} seconds.')
            return render(request, 'core/login.html', {'form': form})

        failed_attempts = cache.get(f'failed_attempts_{email}', 0)

        if failed_attempts >= settings.MAX_LOGIN_ATTEMPTS:
            lockout_time = timezone.now() + datetime.timedelta(seconds=settings.LOCKOUT_TIME)
            cache.set(f'lockout_time_{email}', lockout_time, timeout=settings.LOCKOUT_TIME)
            messages.error(request, f'Account locked due to too many failed attempts. Try again in {settings.LOCKOUT_TIME} seconds.')
            return render(request, 'core/login.html', {'form': form})

        if form.is_valid():
            user = form.get_user()
            if user is not None:
                cache.delete(f'failed_attempts_{email}')
                cache.delete(f'lockout_time_{email}')
                login(request, user)
                messages.success(request, f"Welcome back, {user.username}!")
                return redirect('core:home')

        # If we reach here, authentication has failed
        failed_attempts += 1
        cache.set(f'failed_attempts_{email}', failed_attempts, timeout=24 * 60 * 60)  # 24 hours timeout

        if failed_attempts >= settings.MAX_LOGIN_ATTEMPTS:
            lockout_time = timezone.now() + datetime.timedelta(seconds=settings.LOCKOUT_TIME)
            cache.set(f'lockout_time_{email}', lockout_time, timeout=settings.LOCKOUT_TIME)
            messages.error(request, f'Account locked due to too many failed attempts. Try again in {settings.LOCKOUT_TIME} seconds.')
        else:
            messages.error(request, f'Invalid email or password. {settings.MAX_LOGIN_ATTEMPTS - failed_attempts} attempts remaining.')

    else:
        form = CustomAuthenticationForm()

    return render(request, 'core/login.html', {'form': form})

    return render(request, 'core/login.html', {'form': form})
def custom_logout(request):
    logout(request)
    print("Logout view called") 
    messages.success(request, "You have successfully logged out.")
    return redirect('core:login')  
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user=form.save()
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)
            messages.success(request, 'Account created successfully')
            return redirect('core:home')
    else:
        form = SignUpForm()
    return render(request, 'core/signup.html', {'form': form})




def home(request):
    
    return render(request, 'core/home.html')




# Create your views here.
