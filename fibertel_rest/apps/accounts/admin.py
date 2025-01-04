# apps/accounts/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, ClientProfile

class ClientProfileInline(admin.StackedInline):
    model = ClientProfile
    can_delete = False

class CustomUserAdmin(UserAdmin):
    inlines = (ClientProfileInline,)
    list_display = ('username', 'email', 'is_client', 'is_staff', 'is_active')
    list_filter = ('is_client', 'is_staff', 'is_active')

admin.site.register(User, CustomUserAdmin)
