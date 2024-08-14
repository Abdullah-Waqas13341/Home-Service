from django.contrib import admin
from .models import Seller,Category,Service
@admin.register(Seller)
class sellersAdmin(admin.ModelAdmin):
    list_display = ['username', 'email']
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['seller', 'category', 'title', 'price', 'status', 'avg_rating', 'created_at', 'updated_at', 'admin_action']

# Register your models here.
