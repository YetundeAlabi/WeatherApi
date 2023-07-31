from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', "email", 'verification_code')
    list_filter = ('is_active',)
    fieldsets = (
        (None, {'fields': ['email', 'password']}),
        ('Personal Info', {'fields': ['username']}),
        ('Permissions', {'fields': ('is_active', 'is_superuser')}),
        ("Dates", {"fields": ("last_login",)})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2',),
        }),
    )
