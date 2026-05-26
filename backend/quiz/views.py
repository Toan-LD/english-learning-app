"""
Views for the quiz app.
"""
from django.utils import timezone
from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .models import Quiz, Question, QuizAttempt
from .serializers import (
    QuizSerializer,
    QuizListSerializer,
    QuestionSerializer,
    QuestionWithAnswerSerializer,
    QuizAttemptSerializer,
    QuizSubmitSerializer,
)


class QuizViewSet(viewsets.ModelViewSet):
    """ViewSet for Quiz CRUD operations."""
    queryset = Quiz.objects.filter(is_active=True)
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['quiz_type', 'lesson']
    search_fields = ['title', 'description']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.action == 'list':
            return QuizListSerializer
        return QuizSerializer

    @action(detail=True, methods=['post'])
    def start(self, request, pk=None):
        """Start a new quiz attempt."""
        quiz = self.get_object()

        # Check for existing in-progress attempt
        existing = QuizAttempt.objects.filter(
            user=request.user, quiz=quiz,
            status=QuizAttempt.Status.IN_PROGRESS
        ).first()

        if existing:
            return Response(
                QuizAttemptSerializer(existing).data,
                status=status.HTTP_200_OK,
            )

        attempt = QuizAttempt.objects.create(
            user=request.user,
            quiz=quiz,
            total_questions=quiz.question_count,
            status=QuizAttempt.Status.IN_PROGRESS,
        )
        return Response(
            QuizAttemptSerializer(attempt).data,
            status=status.HTTP_201_CREATED,
        )

    @action(detail=True, methods=['post'])
    def submit(self, request, pk=None):
        """Submit quiz answers and calculate score."""
        quiz = self.get_object()
        serializer = QuizSubmitSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        answers = serializer.validated_data['answers']
        time_taken = serializer.validated_data['time_taken']

        # Get or create attempt
        attempt, created = QuizAttempt.objects.get_or_create(
            user=request.user,
            quiz=quiz,
            status=QuizAttempt.Status.IN_PROGRESS,
            defaults={
                'total_questions': quiz.question_count,
                'time_taken': time_taken,
            }
        )

        if not created:
            attempt.time_taken = time_taken

        # Grade the quiz
        questions = quiz.questions.all()
        correct_count = 0
        total_points = 0
        earned_points = 0

        for question in questions:
            total_points += question.points
            user_answer = answers.get(str(question.id), '')
            if user_answer.strip().lower() == question.correct_answer.strip().lower():
                correct_count += 1
                earned_points += question.points

        # Calculate score
        score = round((earned_points / total_points * 100), 1) if total_points > 0 else 0

        attempt.score = score
        attempt.correct_answers = correct_count
        attempt.answers = answers
        attempt.status = QuizAttempt.Status.COMPLETED
        attempt.completed_at = timezone.now()
        attempt.save()

        # Award XP based on score
        xp_earned = int(score / 10) + correct_count * 2
        request.user.total_xp += xp_earned
        request.user.save(update_fields=['total_xp'])

        # Get questions with answers for review
        questions_with_answers = QuestionWithAnswerSerializer(
            questions, many=True
        ).data

        return Response({
            'attempt': QuizAttemptSerializer(attempt).data,
            'score': score,
            'correct_answers': correct_count,
            'total_questions': quiz.question_count,
            'xp_earned': xp_earned,
            'passed': score >= quiz.passing_score,
            'questions_review': questions_with_answers,
        })


class QuestionViewSet(viewsets.ModelViewSet):
    """ViewSet for Question CRUD operations."""
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['quiz', 'question_type']


class QuizAttemptViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for viewing quiz attempt history."""
    serializer_class = QuizAttemptSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return QuizAttempt.objects.filter(
            user=self.request.user
        ).select_related('quiz')
