from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('login/', views.custom_login, name='login'), 
    path('logout/', views.custom_logout, name='logout'),
    path('signup/', views.signup, name='signup'),
]
