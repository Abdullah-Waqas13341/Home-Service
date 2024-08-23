from django.contrib import admin
from .models import Admin,AdminAction
from sellers.models import Service

@admin.register(Admin)
class AdminAdmin(admin.ModelAdmin):
    list_display = ['username', 'email']
@admin.register(AdminAction)
class AdminActionAdmin(admin.ModelAdmin):
    list_display = ['admin', 'action', 'service', 'created_at']
    list_filter = ['action']
    search_fields = ['admin__username', 'service__title']





class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'seller', 'category', 'price', 'status')
    list_filter = ('status', 'category')
    search_fields = ('title', 'seller__username')
    actions = ['approve_service', 'reject_service']

    def approve_service(self, request, queryset):
        for service in queryset:
            service.status = 'Approved'
            service.save()
            AdminAction.objects.create(
                admin=request.user,
                action=service.status,
                reason=service.admin_comments,
                service=service
            )
        self.message_user(request, "Selected services have been approved.")
    approve_service.short_description = "Approve selected services"

    def reject_service(self, request, queryset):
        for service in queryset:
            service.status = 'Rejected'
            service.save()
            AdminAction.objects.create(
                admin=request.user,
                action=service.status,
                reason=service.admin_comments,
                service=service
            )
        self.message_user(request, "Selected services have been rejected.")
    reject_service.short_description = "Reject selected services"

admin.site.register(Service, ServiceAdmin)


# Register your models here.
