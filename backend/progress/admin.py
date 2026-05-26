"""
Admin configuration for the progress app.
"""
from django.contrib import admin
from .models import UserProgress, DailyActivity


@admin.register(UserProgress)
class UserProgressAdmin(admin.ModelAdmin):
    list_display = [
        'user', 'course', 'status', 'progress_percentage',
        'total_time_spent', 'enrolled_at',
    ]
    list_filter = ['status', 'course']
    search_fields = ['user__email', 'course__title']
    raw_id_fields = ['user', 'course']
    filter_horizontal = ['completed_lessons']


@admin.register(DailyActivity)
class DailyActivityAdmin(admin.ModelAdmin):
    list_display = [
        'user', 'date', 'minutes_studied',
        'words_learned', 'lessons_completed', 'xp_earned',
    ]
    list_filter = ['date']
    search_fields = ['user__email']
    raw_id_fields = ['user']
