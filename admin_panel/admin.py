from django.contrib import admin
from .models import Admin,AdminAction
@admin.register(Admin)
class AdminAdmin(admin.ModelAdmin):
    list_display = ['username', 'email']
@admin.register(AdminAction)
class AdminActionAdmin(admin.ModelAdmin):
    list_display = ['admin', 'action', 'created_at']
# Register your models here.
