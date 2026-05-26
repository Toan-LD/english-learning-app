"""
Views for the progress app.
"""
from datetime import timedelta
from django.utils import timezone
from django.db.models import Avg, Sum
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from courses.models import Course
from .models import UserProgress, DailyActivity
from .serializers import (
    UserProgressSerializer,
    DailyActivitySerializer,
)


class UserProgressViewSet(viewsets.ModelViewSet):
    """ViewSet for UserProgress CRUD operations."""
    serializer_class = UserProgressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserProgress.objects.filter(
            user=self.request.user
        ).select_related('course')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def complete_lesson(self, request, pk=None):
        """Mark a lesson as completed."""
        progress = self.get_object()
        lesson_id = request.data.get('lesson_id')

        if not lesson_id:
            return Response(
                {'error': 'lesson_id is required.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            from courses.models import Lesson
            lesson = Lesson.objects.get(id=lesson_id, course=progress.course)
        except Lesson.DoesNotExist:
            return Response(
                {'error': 'Lesson not found in this course.'},
                status=status.HTTP_404_NOT_FOUND,
            )

        progress.completed_lessons.add(lesson)
        progress.update_progress()
        progress.last_activity_at = timezone.now()
        progress.status = UserProgress.EnrollmentStatus.IN_PROGRESS

        # Check if course is completed
        if progress.progress_percentage >= 100:
            progress.status = UserProgress.EnrollmentStatus.COMPLETED
            progress.completed_at = timezone.now()
            # Award completion XP
            request.user.total_xp += 50
            request.user.save(update_fields=['total_xp'])

        progress.save()

        # Update daily activity
        today = timezone.now().date()
        activity, _ = DailyActivity.objects.get_or_create(
            user=request.user, date=today,
            defaults={'lessons_completed': 0}
        )
        activity.lessons_completed += 1
        activity.xp_earned += 10
        activity.save()

        return Response(UserProgressSerializer(progress).data)

    @action(detail=True, methods=['post'])
    def log_time(self, request, pk=None):
        """Log study time for a course."""
        progress = self.get_object()
        minutes = request.data.get('minutes', 0)

        progress.total_time_spent += int(minutes)
        progress.last_activity_at = timezone.now()
        progress.save(update_fields=['total_time_spent', 'last_activity_at'])

        # Update daily activity
        today = timezone.now().date()
        activity, _ = DailyActivity.objects.get_or_create(
            user=request.user, date=today
        )
        activity.minutes_studied += int(minutes)
        activity.save()

        return Response(UserProgressSerializer(progress).data)


class DailyActivityViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for viewing daily activity history."""
    serializer_class = DailyActivitySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return DailyActivity.objects.filter(user=self.request.user)


class ProgressStatsView(viewsets.ViewSet):
    """ViewSet for progress statistics."""
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        """Get comprehensive progress statistics."""
        user = request.user
        from quiz.models import QuizAttempt
        from vocabulary.models import UserWord

        # Course progress
        enrollments = UserProgress.objects.filter(user=user)
        courses_completed = enrollments.filter(
            status=UserProgress.EnrollmentStatus.COMPLETED
        ).count()

        # Quiz statistics
        quiz_attempts = QuizAttempt.objects.filter(
            user=user, status='completed'
        )
        avg_score = quiz_attempts.aggregate(avg=Avg('score'))['avg'] or 0

        # Vocabulary
        words_learned = UserWord.objects.filter(
            user=user, is_learned=True
        ).count()

        # Weekly activity (last 7 days)
        today = timezone.now().date()
        week_ago = today - timedelta(days=6)
        weekly = DailyActivity.objects.filter(
            user=user, date__gte=week_ago
        ).order_by('date')

        # Total study time
        total_time = enrollments.aggregate(
            total=Sum('total_time_spent')
        )['total'] or 0

        return Response({
            'total_courses_enrolled': enrollments.count(),
            'courses_completed': courses_completed,
            'total_words_learned': words_learned,
            'total_quizzes_taken': quiz_attempts.count(),
            'average_quiz_score': round(float(avg_score), 1),
            'total_study_time': total_time,
            'current_streak': user.streak_days,
            'total_xp': user.total_xp,
            'learning_level': user.learning_level,
            'weekly_activity': DailyActivitySerializer(
                weekly, many=True
            ).data,
        })
