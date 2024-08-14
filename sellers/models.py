from django.db import models
from core.models import User
from admin_panel.models import AdminAction
class Seller(User):
    pass

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    

class Service(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    category=models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.FloatField()
    status = models.CharField(max_length=20, default='Pending',choices=[('Available', 'Available'), ('Not Available', 'Not Available')])
    avg_rating = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    admin_action=models.OneToOneField(AdminAction, on_delete=models.CASCADE, null=True, blank=True)
    class Meta:
        ordering = ['-created_at']

# Create your models here.
