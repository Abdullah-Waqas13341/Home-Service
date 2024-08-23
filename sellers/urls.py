from django.urls import path
from .views import services, post_service,list_services,booked_services,accept_booking,decline_booking
app_name = 'seller'
urlpatterns = [
    path('', services, name='services'),
    path('post-service/', post_service, name='post_service'),
    path('list-services/', list_services, name='list_services'),
    path('booked-services/', booked_services, name='booked_services'),
    path('accept_booking/<int:booking_id>/', accept_booking, name='accept_booking'),
    path('decline_booking/<int:booking_id>/',decline_booking, name='decline_booking'),

]