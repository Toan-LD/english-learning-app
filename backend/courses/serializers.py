"""
Serializers for the courses app.
"""
from rest_framework import serializers
from .models import Course, Lesson


class LessonSerializer(serializers.ModelSerializer):
    """Serializer for Lesson model."""
    course_title = serializers.CharField(source='course.title', read_only=True)

    class Meta:
        model = Lesson
        fields = [
            'id', 'course', 'course_title', 'title', 'slug',
            'content', 'lesson_type', 'order', 'duration_minutes',
            'video_url', 'is_free', 'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class LessonListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for lesson listing."""

    class Meta:
        model = Lesson
        fields = [
            'id', 'title', 'slug', 'lesson_type',
            'order', 'duration_minutes', 'is_free',
        ]


class CourseSerializer(serializers.ModelSerializer):
    """Serializer for Course model with nested lessons."""
    lessons = LessonListSerializer(many=True, read_only=True)
    lesson_count = serializers.ReadOnlyField()
    created_by_name = serializers.CharField(
        source='created_by.full_name', read_only=True, default=''
    )

    class Meta:
        model = Course
        fields = [
            'id', 'title', 'slug', 'description', 'thumbnail',
            'difficulty', 'is_published', 'total_lessons',
            'estimated_hours', 'created_by', 'created_by_name',
            'lesson_count', 'lessons', 'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class CourseListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for course listing."""
    lesson_count = serializers.ReadOnlyField()

    class Meta:
        model = Course
        fields = [
            'id', 'title', 'slug', 'description', 'thumbnail',
            'difficulty', 'total_lessons', 'estimated_hours',
            'lesson_count', 'created_at',
        ]
