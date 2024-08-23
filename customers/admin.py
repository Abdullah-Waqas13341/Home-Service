from django.contrib import admin
from .models import Booking, Customer, Review,Payment
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['username', 'email']
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['customer', 'service', 'date', 'time', 'service_date', 'status','payment_status']
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['booking', 'amount', 'payment_date', 'payment_status', 'payment_mode']
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['customer', 'service', 'rating', 'review']
# Register your models here.
