from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    GENDER_CHOICES = [('M', 'Male'), ('F', 'Female',)]
    ROLE_CHOICES = [('customer', 'Customer'), ('seller', 'Seller'),('admin', 'Admin')]
    email = models.EmailField(unique=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    age = models.PositiveIntegerField(null=True,blank=True)
    role = models.CharField(max_length=10,choices=[(role[0], role[1]) for role in ROLE_CHOICES[:2]])
    date_joined = models.DateTimeField(auto_now_add=True)





