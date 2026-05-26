"""
Admin configuration for the quiz app.
"""
from django.contrib import admin
from .models import Quiz, Question, QuizAttempt


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'quiz_type', 'time_limit',
        'passing_score', 'is_active', 'created_at',
    ]
    list_filter = ['quiz_type', 'is_active']
    search_fields = ['title', 'description']
    inlines = [QuestionInline]


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = [
        'quiz', 'question_text', 'question_type',
        'correct_answer', 'points', 'order',
    ]
    list_filter = ['question_type', 'quiz']
    search_fields = ['question_text', 'correct_answer']


@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = [
        'user', 'quiz', 'score', 'correct_answers',
        'total_questions', 'status', 'started_at',
    ]
    list_filter = ['status', 'quiz']
    search_fields = ['user__email', 'quiz__title']
    raw_id_fields = ['user', 'quiz']
