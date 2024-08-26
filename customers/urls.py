from django.urls import path
from .views import services_list, service_detail, payment_view,payment_success,booked_services,review_form
from core.views import custom_logout
app_name = 'customers'

urlpatterns = [

    path('services/', services_list, name='services_list'),
    path('services/<int:service_id>/', service_detail, name='service_detail'),
    path('payment/<int:booking_id>',payment_view, name='payment_view'),
    path('payment_success/', payment_success, name='payment_success'),
    path('booked_services/',booked_services, name='booked_services'),
    path('review_form/<int:service_id>',review_form, name='review_form'),
]
