"""
Views for the courses app.
"""
from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .models import Course, Lesson
from .serializers import (
    CourseSerializer,
    CourseListSerializer,
    LessonSerializer,
)


class CourseViewSet(viewsets.ModelViewSet):
    """ViewSet for Course CRUD operations."""
    queryset = Course.objects.filter(is_published=True)
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['difficulty', 'is_published']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'title', 'difficulty']
    ordering = ['-created_at']
    lookup_field = 'slug'

    def get_serializer_class(self):
        if self.action == 'list':
            return CourseListSerializer
        return CourseSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=['get'])
    def lessons(self, request, slug=None):
        """Get all lessons for a course."""
        course = self.get_object()
        lessons = course.lessons.all().order_by('order')
        serializer = LessonSerializer(lessons, many=True)
        return Response(serializer.data)


class LessonViewSet(viewsets.ModelViewSet):
    """ViewSet for Lesson CRUD operations."""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['course', 'lesson_type']
    search_fields = ['title', 'content']
    ordering = ['order']
