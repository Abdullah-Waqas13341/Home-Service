from django.db import models
from core.models import User
from sellers.models import Service
from datetime import date
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator


class Customer(User):
    pass


class Booking(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    date = models.DateField(default=date.today)
    time = models.TimeField()
    service_date = models.DateField()
    address = models.TextField()

    status = models.CharField(max_length=20, default='pending', choices=[
        ('accepted', 'Accepted'),
        ('declined', 'Declined'),
        ('pending', 'Pending'),
    ])

    progress = models.CharField(max_length=20, default='pending', choices=[
        ('completed', 'Completed'),
        ('on-going', 'On-going'),
        ('pending', 'Pending'),
    ])

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    payment_status = models.CharField(max_length=20, default='Unpaid', choices=[
        ('paid', 'Paid'),
        ('pending', 'Pending'),
        ('unpaid', 'Unpaid')
    ])

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.service.title

    def clean(self):
        if self.service_date < timezone.now().date():
            raise ValidationError("Service date cannot be in the past.")


class Payment(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    stripe_charge_id = models.CharField(max_length=100, blank=True, null=True)

    PAYMENT_STATUS_CHOICES = [
        ('paid', 'Paid'),
        ('pending', 'Pending'),
        ('unpaid', 'Unpaid'),
    ]
    payment_status = models.CharField(max_length=20, default='Unpaid', choices=PAYMENT_STATUS_CHOICES)

    PAYMENT_MODE_CHOICES = [
        ('Card', 'Card'),
        ('Cash', 'Cash'),
    ]
    payment_mode = models.CharField(max_length=20, default='Card', choices=PAYMENT_MODE_CHOICES)

    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(Customer, null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        ordering = ['-payment_date']


class Review(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, null=True, blank=True)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    review = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
