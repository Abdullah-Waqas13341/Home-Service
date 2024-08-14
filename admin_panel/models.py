from django.db import models
from core.models import User
class Admin(User):
    class Meta:
        
        proxy = True

    def save(self, *args, **kwargs):
        self.role = 'admin'
        super(Admin, self).save(*args, **kwargs)
    


class AdminAction(models.Model):
    admin= models.ForeignKey(Admin, on_delete=models.CASCADE)
    ACTION_CHOICES = [('Approve', 'Approve'), ('Reject', 'Reject'), ('Pending', 'Pending')]
    action = models.CharField(max_length=10, choices=ACTION_CHOICES)
    reason = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ['-created_at']

# Create your models here.