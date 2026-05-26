"""
Admin configuration for the vocabulary app.
"""
from django.contrib import admin
from .models import Word, UserWord


@admin.register(Word)
class WordAdmin(admin.ModelAdmin):
    list_display = [
        'word', 'part_of_speech', 'difficulty',
        'is_active', 'created_at',
    ]
    list_filter = ['part_of_speech', 'difficulty', 'is_active']
    search_fields = ['word', 'definition', 'example_sentence']


@admin.register(UserWord)
class UserWordAdmin(admin.ModelAdmin):
    list_display = [
        'user', 'word', 'is_learned', 'review_status',
        'times_reviewed', 'last_reviewed_at',
    ]
    list_filter = ['is_learned', 'review_status']
    search_fields = ['user__email', 'word__word']
    raw_id_fields = ['user', 'word']
