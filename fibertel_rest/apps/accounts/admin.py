from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, ClientProfile

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_client', 'is_staff', 'created_at')
    list_filter = ('is_client', 'is_staff', 'is_active', 'created_at')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('-created_at',)

    fieldsets = UserAdmin.fieldsets + (
        ('Custom Fields', {'fields': ('phone_number', 'is_client')}),
    )

@admin.register(ClientProfile)
class ClientProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'document_type', 'document_number', 'service_status')
    list_filter = ('document_type', 'service_status')
    search_fields = ('user__username', 'user__email', 'document_number')