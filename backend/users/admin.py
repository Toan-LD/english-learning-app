"""
Admin configuration for the users app.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Custom admin for User model."""
    list_display = [
        'email', 'username', 'first_name', 'last_name',
        'learning_level', 'streak_days', 'total_xp', 'is_staff',
    ]
    list_filter = ['learning_level', 'is_staff', 'is_active', 'is_notification_enabled']
    search_fields = ['email', 'username', 'first_name', 'last_name']
    ordering = ['-created_at']

    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        (_('Personal info'), {
            'fields': ('first_name', 'last_name', 'bio', 'avatar')
        }),
        (_('Learning'), {
            'fields': (
                'learning_level', 'daily_goal', 'streak_days',
                'last_active_date', 'total_xp', 'is_notification_enabled',
            )
        }),
        (_('Permissions'), {
            'fields': (
                'is_active', 'is_staff', 'is_superuser',
                'groups', 'user_permissions',
            ),
        }),
        (_('Important dates'), {
            'fields': ('last_login', 'date_joined')
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 'username', 'first_name', 'last_name',
                'password1', 'password2', 'learning_level',
            ),
        }),
    )
