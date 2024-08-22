from django.urls import path
from .views import services, post_service
app_name = 'seller'
urlpatterns = [
    path('', services, name='services'),
    path('post-service/', post_service, name='post_service'),
    
]