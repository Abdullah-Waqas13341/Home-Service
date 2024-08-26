from django.shortcuts import render, redirect,get_object_or_404
from .forms import ServiceForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Service 
from admin_panel.models import AdminAction
from customers.models import Booking, Review
@login_required(login_url='core:login')
def services(request):
    return render(request, 'sellers/services.html')
@login_required(login_url='core:login')
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

@login_required(login_url='core:login')
def list_services(request):
    services = Service.objects.filter(seller=request.user.seller)
    return render(request, 'sellers/list_services.html', {'services': services})
@login_required(login_url='core:login')


def booked_services(request):
    # Get all bookings for the current seller
    bookings = Booking.objects.filter(service__seller=request.user.seller).order_by('-created_at')
    
    # Get all reviews for these bookings
    reviews = Review.objects.filter(booking__in=bookings)
    
    # Create a dictionary mapping booking IDs to their reviews
    reviews_dict = {review.booking.id: review.review for review in reviews}
    
    # Create a list of tuples with (booking, associated review or None)
    bookings_reviews = [(booking, reviews_dict.get(booking.id)) for booking in bookings]
    
    # Pass the list to the template context
    return render(request, 'sellers/booked_services.html', {'bookings_reviews': bookings_reviews})




@login_required(login_url='core:login')
def accept_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    
    
    booking.status = 'Accepted'
    booking.progress = 'On-going'
    booking.save()

    messages.success(request, 'Booking has been accepted.')
    return redirect('sellers:booked_services',) 
@login_required(login_url='core:login')
def decline_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    
   
    booking.status = 'Declined'
    booking.save()

    messages.success(request, 'Booking has been declined.')
    return redirect('sellers:booked_services')  

@login_required(login_url='core:login')
def complete_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    booking.progress = 'Completed'
    booking.save()
    return redirect('sellers:booked_services')

@login_required(login_url='core:login')
def request_review(request, service_id):

    service=Service.objects.get(id=service_id)

    if service.status == 'Rejected' and service.seller == request.user.seller:
      
        service.status = 'Pending'
        service.save()

        messages.success(request, 'Review requested successfully. The admin will review your service.')

    else:
        messages.error(request, 'You are not allowed to request a review for this service.')


    return redirect('sellers:list_services')
 
# Create your views here.
