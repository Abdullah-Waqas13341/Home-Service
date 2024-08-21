from django.db import models
from core.models import User

from core.models import User

class Admin(User):
    role=None
    admin_role = models.CharField(
        max_length=10,
        choices=[('Admin', 'Admin')],
        default='Admin',
    )
   


    class Meta:
        verbose_name = "Admin"
        verbose_name_plural = "Admins"

    def get_role_display(self):
        return "Admin"



class AdminAction(models.Model):
    admin= models.ForeignKey(Admin, on_delete=models.CASCADE)
    ACTION_CHOICES = [('Approve', 'Approve'), ('Reject', 'Reject'), ('Pending', 'Pending')]
    action = models.CharField(max_length=10, choices=ACTION_CHOICES)
    reason = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    service = models.ForeignKey('sellers.Service', on_delete=models.CASCADE,default=None)
    class Meta:
        ordering = ['-created_at']

# Create your models here.