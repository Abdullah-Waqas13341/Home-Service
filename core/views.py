# Create your views here.
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import render, redirect
from django.utils import timezone
from django.core.cache import cache
from .forms import CustomAuthenticationForm, SignUpForm
from django.contrib.auth import logout
from django.conf import settings




def custom_logout(request):
    logout(request)
    print("Logout view called") 
    messages.success(request, "You have successfully logged out.")
    return redirect('core:login')  

def custom_login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')  
            password = form.cleaned_data.get('password')
            
            
            lockout_time = cache.get(f'lockout_time_{email}')
            if lockout_time and timezone.now() < lockout_time:
                messages.error(request, 'Your account is locked. Please try again later.')
                return render(request, 'core/login.html', {'form': form})
            print(f"Email: {email}, Password: {password}")

            user = authenticate(request, email=email, password=password)
            if user is not None:
           
                cache.delete(f'failed_attempts_{email}')
                cache.delete(f'lockout_time_{email}')

                login(request, user)
                messages.success(request, f"Welcome back, {user.username}!")
                return redirect('core:home')
            else:
               
                failed_attempts = cache.get(f'failed_attempts_{email}', 0) + 1
                cache.set(f'failed_attempts_{email}', failed_attempts, settings.LOCKOUT_TIME)

                if failed_attempts >= settings.MAX_ATTEMPTS:
                    lockout_time = timezone.now() + timezone.timedelta(seconds=settings.LOCKOUT_TIME)
                    cache.set(f'lockout_time_{email}', lockout_time, settings.LOCKOUT_TIME)
                    messages.error(request, 'Account locked due to too many failed attempts. Try again in 5 minutes.')
                else:
                    messages.error(request, 'Invalid email or password.')
        else:
            messages.error(request, 'Invalid email or password.')
    else:
        form = CustomAuthenticationForm()

    return render(request, 'core/login.html', {'form': form})

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




# core/views.py


def home(request):
    
    return render(request, 'core/home.html')




# Create your views here.
