
# customer/views.py
from django.contrib.auth import logout as auth_logout
import stripe
from django.conf import settings
from sellers.models import Service, Category
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from customers.models import Booking, Payment, Review
from .forms import BookingForm, PaymentForm, ReviewForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse

@login_required(login_url='core:login')
def service_detail(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    booking_created = request.GET.get('booking_created', False)== 'True'

    booking = None  
    if request.user.is_authenticated:
        booking = Booking.objects.filter(customer=request.user.customer, service=service).first()
   
    if request.method == 'POST' and 'book_service' in request.POST:
        booking_form = BookingForm(request.POST)
        if booking_form.is_valid():
            booking = booking_form.save(commit=False)
            booking.customer = request.user.customer  
            booking.service = service
            booking.save()
            messages.success(request, 'Your booking has been confirmed.')
            booking_created = True  
            return redirect(f"{request.path}?booking_created=True")
  
    else:
        booking_form = BookingForm()

    
   

    return render(request, 'customers/service_detail.html', {
        'service': service,
        'booking_form': booking_form,
        'booking_created': booking_created,
        'booking': booking,  
    })


@login_required(login_url='core:login')
def review_form(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    
    # Find the most recent booking for this service and customer
    booking = Booking.objects.filter(
        service=service,
        customer=request.user.customer
    ).order_by('-created_at').first()

    if not booking:
        messages.error(request, 'You need to book this service before leaving a review.')
        return redirect('customers:service_detail', service_id=service.id)

    if request.method == 'POST' and 'submit_review' in request.POST:
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.customer = request.user.customer
            review.service = service
            review.booking = booking
            review.save()
            messages.success(request, 'Your review has been submitted.')
            return redirect('customers:service_detail', service_id=service.id)
    else:
        review_form = ReviewForm()

    context = {
        'review_form': review_form,
        'service': service,
        'booking': booking
    }
    return render(request, 'customers/review_form.html', context)
@login_required(login_url='core:login')
def services_list(request):
    selected_category = request.GET.get('category')
    sort_order = request.GET.get('sort_order', 'desc')  

    
    services = Service.objects.filter(status='Approved')
    if selected_category:
        services = services.filter(category_id=selected_category)

    
    if sort_order == 'asc':
        services = services.order_by('created_at')
    else:
        services = services.order_by('-created_at')

   
    paginator = Paginator(services, 6)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

   
    categories = Category.objects.all()

    return render(request, 'customers/services_list.html', {
        'page_obj': page_obj,
        'categories': categories,
        'selected_category': int(selected_category) if selected_category else None,
        'sort_order': sort_order,
    })

@login_required(login_url='core:login')
def booked_services(request):

    bookings = Booking.objects.filter(customer=request.user.customer)
    

    for booking in bookings:
        try:
  
            payment = Payment.objects.get(booking=booking)
            booking.payment_status = payment.payment_status
            booking.save()
            print("eee",booking.payment_status)

        except Payment.DoesNotExist:
         
            booking.payment_status = 'Unpaid'
          
        booking.payment_url = reverse('customers:payment_view', args=[booking.id])

    return render(request, 'customers/booked_services.html', {'bookings': bookings})

   



stripe.api_key = settings.STRIPE_SECRET_KEY

@login_required(login_url='core:login')
def payment_view(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            try:
               
                charge = stripe.Charge.create(
                    amount=int(amount * 100),  
                    currency='pkr',
                    description='Payment for Booking ID {}'.format(booking_id),
                    source=request.POST['stripeToken'],
                    
                )
                
                
                payment= Payment.objects.create(
                    amount=amount,
                    stripe_charge_id=charge.id,
                    booking=booking ,
                    
                     
                )
                payment.payment_status = 'paid'
                payment.save()
                messages.success(request, 'Payment successful!')
                return redirect('customers:payment_success')
            except stripe.error.StripeError as e:
                messages.error(request, f"Payment error: {e}")
                return redirect('customers:payment_view', booking_id=booking_id)
    else:
        form = PaymentForm()

    return render(request, 'customers/payment.html', {
        'form': form,
        'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY,
        'booking': booking
    })

def payment_success(request):
    return render(request, 'customers/payment_success.html')







def ongoing_services(request):
   
    pass

def completed_services(request):
 
    pass

def logout_view(request):
    auth_logout(request)
    return redirect('services_list')  



# Create your views here.
