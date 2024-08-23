from django.shortcuts import render, redirect,get_object_or_404
from .forms import ServiceForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Service 
from customers.models import Booking
@login_required
def services(request):
    return render(request, 'sellers/services.html')
@login_required
def post_service(request):

    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            try:
                service = form.save(commit=False)
                service.seller = request.user.seller
                service.status = 'Pending'
                service.save()
                messages.success(request, 'Service posted successfully')
                return redirect('sellers:services')
            except Exception as e:
                messages.error(request, f'Error occurred while posting service: {str(e)}')
        else:
            messages.error(request, 'Invalid form data')
    else:
        form = ServiceForm()
    
    return render(request, 'sellers/post_service.html', {'form': form})

@login_required
def list_services(request):
    services = Service.objects.filter(seller=request.user.seller)
    return render(request, 'sellers/list_services.html', {'services': services})
@login_required
def booked_services(request):
    bookings=Booking.objects.filter(service__seller=request.user.seller)
    return render(request, 'sellers/booked_services.html', {'bookings': bookings})

@login_required
def accept_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    
    # Update the booking status
    booking.status = 'Accepted'
    booking.save()

    messages.success(request, 'Booking has been accepted.')
    return redirect('sellers:booked_services')  # Replace with the name of your bookings page
@login_required
def decline_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    
    # Update the booking status
    booking.status = 'Declined'
    booking.save()

    messages.success(request, 'Booking has been declined.')
    return redirect('sellers:booked_services')  # Replace with the name of your bookings page

    
    
# Create your views here.
