"""
Serializers for the progress app.
"""
from rest_framework import serializers
from .models import UserProgress, DailyActivity


class UserProgressSerializer(serializers.ModelSerializer):
    """Serializer for UserProgress model."""
    course_title = serializers.CharField(source='course.title', read_only=True)
    course_slug = serializers.CharField(source='course.slug', read_only=True)
    course_thumbnail = serializers.ImageField(
        source='course.thumbnail', read_only=True
    )
    total_lessons = serializers.IntegerField(
        source='course.lesson_count', read_only=True
    )
    completed_lesson_count = serializers.SerializerMethodField()

    class Meta:
        model = UserProgress
        fields = [
            'id', 'user', 'course', 'course_title', 'course_slug',
            'course_thumbnail', 'status', 'progress_percentage',
            'total_time_spent', 'total_lessons', 'completed_lesson_count',
            'enrolled_at', 'last_activity_at', 'completed_at',
        ]
        read_only_fields = [
            'id', 'user', 'progress_percentage',
            'enrolled_at', 'last_activity_at', 'completed_at',
        ]

    def get_completed_lesson_count(self, obj) -> int:
        return obj.completed_lessons.count()


class DailyActivitySerializer(serializers.ModelSerializer):
    """Serializer for DailyActivity model."""

    class Meta:
        model = DailyActivity
        fields = [
            'id', 'user', 'date', 'minutes_studied',
            'words_learned', 'lessons_completed',
            'quizzes_taken', 'xp_earned',
        ]
        read_only_fields = ['id', 'user']


class ProgressStatsSerializer(serializers.Serializer):
    """Serializer for progress statistics."""
    total_courses_enrolled = serializers.IntegerField()
    courses_completed = serializers.IntegerField()
    total_lessons_completed = serializers.IntegerField()
    total_words_learned = serializers.IntegerField()
    total_quizzes_taken = serializers.IntegerField()
    average_quiz_score = serializers.FloatField()
    total_study_time = serializers.IntegerField()
    current_streak = serializers.IntegerField()
    weekly_activity = DailyActivitySerializer(many=True)
