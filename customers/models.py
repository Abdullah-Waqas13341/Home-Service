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
    
class Payment(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE)
    amount = models.FloatField()
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_status= models.CharField(max_length=20, default='Pending',choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Cancelled', 'Cancelled')])
    payment_mode= models.CharField(max_length=20, default='Cash',choices=[('Cash', 'Cash'), ('Card', 'Card'), ('Net Banking', 'Net Banking')])
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
