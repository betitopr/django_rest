from django.contrib import admin
from .models import InternetPlan, ClientService

@admin.register(InternetPlan)
class InternetPlanAdmin(admin.ModelAdmin):
    list_display = (
        'name', 
        'download_speed', 
        'upload_speed', 
        'price', 
        'is_active'
    )
    list_filter = ('is_active',)
    search_fields = ('name',)
    ordering = ('price',)
    
    fieldsets = (
        ('Plan Information', {
            'fields': ('name', 'description')
        }),
        ('Speed Details', {
            'fields': ('download_speed', 'upload_speed')
        }),
        ('Commercial Information', {
            'fields': ('price', 'is_active')
        })
    )

@admin.register(ClientService)
class ClientServiceAdmin(admin.ModelAdmin):
    list_display = (
        'get_client_name',
        'plan',
        'status',
        'installation_date',
        'next_payment_date'
    )
    list_filter = ('status', 'plan')
    search_fields = (
        'client__username',
        'client__email',
        'ip_address'
    )
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Client Information', {
            'fields': ('client', 'plan')
        }),
        ('Service Details', {
            'fields': (
                'status',
                'installation_date',
                'ip_address',
                'mac_address'
            )
        }),
        ('Payment Information', {
            'fields': (
                'last_payment_date',
                'next_payment_date'
            )
        })
    )

    def get_client_name(self, obj):
        return obj.client.get_full_name()
    get_client_name.short_description = 'Client Name'

    # Acciones personalizadas
    actions = ['suspend_services', 'activate_services']

    def suspend_services(self, request, queryset):
        queryset.update(status='suspended')
    suspend_services.short_description = "Suspend selected services"

    def activate_services(self, request, queryset):
        queryset.update(status='active')
    activate_services.short_description = "Activate selected services"