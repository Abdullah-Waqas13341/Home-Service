from django.shortcuts import redirect
from django.urls import reverse
import re

class RoleBasedRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and request.path != reverse('core:logout'):
            if request.user.role == 'customer':
                allowed_urls = [
                    reverse('customers:services_list'),
                    reverse('customers:booked_services'),
                    reverse('customers:payment_success'),
                ]

                # Check if the URL matches the pattern for payment_view
                payment_pattern = re.compile(r'^' + reverse('customers:payment_view', kwargs={'booking_id': 1}).replace('1', r'\d+') + r'$')
                
                if any(payment_pattern.match(request.path) or request.path.startswith(url) for url in allowed_urls):
                    pass
                else:
                    return redirect('customers:services_list')
            elif request.user.role == 'seller':
                allowed_urls = [
                    reverse('seller:services'),
                    reverse('seller:post_service'),
                    reverse('seller:list_services'),
                ]

                if not any(request.path.startswith(url) for url in allowed_urls):
                    return redirect('seller:services')
        
        response = self.get_response(request)
        return response
