"""
Admin configuration for the courses app.
"""
from django.contrib import admin
from .models import Course, Lesson


class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'difficulty', 'is_published',
        'total_lessons', 'estimated_hours', 'created_at',
    ]
    list_filter = ['difficulty', 'is_published']
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [LessonInline]


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'course', 'lesson_type', 'order',
        'duration_minutes', 'is_free',
    ]
    list_filter = ['lesson_type', 'course', 'is_free']
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
