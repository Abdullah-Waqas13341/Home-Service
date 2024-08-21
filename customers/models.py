from django.db import models
from core.models import User
from sellers.models import Service

class Customer(User):
    pass
class Booking(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    service_date = models.DateField()
    address = models.TextField()
    status = models.CharField(max_length=20, default='Pending',choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Cancelld', 'Cancelld')])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ['-created_at']
    def __str__(self):
        return self.service.title
    
class Payment(models.Model):
   
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    stripe_charge_id = models.CharField(max_length=100, blank=True, null=True)
    PAYMENT_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Cancelled', 'Cancelled'),
        ('Failed', 'Failed'),
        ('Refunded', 'Refunded'),
    ]
    payment_status = models.CharField(max_length=20, default='Pending', choices=PAYMENT_STATUS_CHOICES)
    PAYMENT_MODE_CHOICES = [
        ('Cash', 'Cash'),
        ('Card', 'Card'),
        ('Net Banking', 'Net Banking'),
    ]
    payment_mode = models.CharField(max_length=20, default='Cash', choices=PAYMENT_MODE_CHOICES)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(Customer, null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        ordering = ['-payment_date']


    
class Review(models.Model):
    customer= models.ForeignKey(Customer, on_delete=models.CASCADE)
    service= models.ForeignKey(Service, on_delete=models.CASCADE)
    rating = models.IntegerField()
    review = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ['-created_at']

# Create your models here.
