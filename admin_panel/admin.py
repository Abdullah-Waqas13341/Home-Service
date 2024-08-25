from django.contrib import admin
from .models import Admin, AdminAction
from sellers.models import Service,Category
from django.contrib.admin import AdminSite
from django.urls import path
from django.template.response import TemplateResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.html import format_html

@admin.register(Admin)
class AdminAdmin(admin.ModelAdmin):
    list_display = ['username', 'email']

@admin.register(AdminAction)
class AdminActionAdmin(admin.ModelAdmin):
    list_display = ['admin', 'action', 'service', 'created_at']
    list_filter = ['action']
    search_fields = ['admin__username', 'service__title']

def approve_services(modeladmin, request, queryset):
    queryset.update(status='Approved')
    for service in queryset:
        AdminAction.objects.create(service=service, action='Approved')
    modeladmin.message_user(request, "Selected services have been approved.")

def reject_services(modeladmin, request, queryset):
    queryset.update(status='Rejected')
    for service in queryset:
        AdminAction.objects.create(service=service, action='Rejected')
    modeladmin.message_user(request, "Selected services have been rejected.")

approve_services.short_description = "Approve selected services"
reject_services.short_description = "Reject selected services"

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'status')
    actions = [approve_services, reject_services]

# admin_panel/admin.py

class MyAdminSite(admin.AdminSite):
    site_header = "Admin Dashboard"
    login_template = 'admin/login.html'
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('notifications/', self.admin_view(self.notifications_view), name='notifications'),
        ]
        return custom_urls + urls

    def notifications_view(self, request):
        if request.method == 'POST':
            if 'approve' in request.POST or 'reject' in request.POST:
                service_id = request.POST.get('approve') or request.POST.get('reject')
                action = 'Approved' if 'approve' in request.POST else 'Rejected'
                comments = request.POST.get(f'comments_{service_id}', '')  # Get comments if present
                
                service = Service.objects.get(id=service_id)
                service.status = action
                service.admin_comments = comments  # Save comments
                service.save()

                if request.user.is_superuser:  # Ensure the user is a superuser
                    AdminAction.objects.create(
                        admin=request.user,  # Set the current superuser
                        service=service,
                        action=action,
                         # Save comments if desired
                    )

            return HttpResponseRedirect(request.path)
        pending_services = Service.objects.filter(status='Pending')
        context = dict(
            self.each_context(request),
            pending_services=pending_services,
        )
        return TemplateResponse(request, 'admin_panel/notifications.html', context)
        
    def get_app_list(self, request):
        app_list = super().get_app_list(request)
        custom_app = {
            'name': 'Custom Actions',
            'app_label': 'custom_actions',
            'models': [{
                'name': 'Notifications',
                'object_name': 'notifications',
                'admin_url': reverse('admin:notifications'),
                'view_only': True,
            }],
        }
        app_list.append(custom_app)
        return app_list

    def each_context(self, request):
        context = super().each_context(request)
        context['notifications_button'] = self.notifications_button(request)
        return context

    def notifications_button(self, request):
        url = reverse('admin:notifications')
        return format_html(
            '<a href="{}" class="button" style="margin-left: 10px;">Notifications</a>',
            url
        )



admin_site = MyAdminSite(name='myadmin')

admin_site.register(Service, ServiceAdmin)
admin_site.register(Category)
# Register your models here
admin_site.register(Admin, AdminAdmin)
admin_site.register(AdminAction, AdminActionAdmin)
