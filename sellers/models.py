from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from core.models import User


class Seller(User):
    pass


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name


class Service(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    AVAILABILITY_CHOICES = [
        ('available', 'Available'),
        ('not available', 'Not Available'),
    ]

    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.FloatField(validators=[MinValueValidator(0.0)])
    status = models.CharField(max_length=20, default='Pending', choices=STATUS_CHOICES)
    availability = models.CharField(max_length=15, default='Available', choices=AVAILABILITY_CHOICES)
    avg_rating = models.FloatField(default=0, validators=[MinValueValidator(0.0), MaxValueValidator(5.0)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    admin_comments = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-created_at']

    def clean(self):
        # Ensure availability is only set when approved
        if self.status != 'Approved' and self.availability == 'Available':
            raise ValidationError("Service must be approved before it can be available.")

    def save(self, *args, **kwargs):
        self.full_clean()  # call clean() before saving
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
