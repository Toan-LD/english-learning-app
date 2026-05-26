"""
Views for the vocabulary app.
"""
from datetime import timedelta
from django.utils import timezone
from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .models import Word, UserWord
from .serializers import (
    WordSerializer,
    WordListSerializer,
    UserWordSerializer,
    UserWordUpdateSerializer,
)


class WordViewSet(viewsets.ModelViewSet):
    """ViewSet for Word CRUD operations."""
    queryset = Word.objects.filter(is_active=True)
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['part_of_speech', 'difficulty']
    search_fields = ['word', 'definition', 'example_sentence']
    ordering_fields = ['word', 'difficulty', 'created_at']
    ordering = ['word']

    def get_serializer_class(self):
        if self.action == 'list':
            return WordListSerializer
        return WordSerializer

    @action(detail=True, methods=['post'])
    def mark_learned(self, request, pk=None):
        """Mark a word as learned for the current user."""
        word = self.get_object()
        user_word, created = UserWord.objects.get_or_create(
            user=request.user, word=word
        )
        user_word.is_learned = True
        user_word.review_status = UserWord.ReviewStatus.MASTERED
        user_word.last_reviewed_at = timezone.now()
        user_word.save()

        # Award XP
        request.user.total_xp += 5
        request.user.save(update_fields=['total_xp'])

        return Response({
            'message': f'Word "{word.word}" marked as learned!',
            'xp_earned': 5,
        })

    @action(detail=False, methods=['get'])
    def random(self, request):
        """Get random words for flashcard practice."""
        count = int(request.query_params.get('count', 10))
        count = min(count, 50)  # Limit to 50
        difficulty = request.query_params.get('difficulty', None)

        queryset = Word.objects.filter(is_active=True)
        if difficulty:
            queryset = queryset.filter(difficulty=difficulty)

        words = queryset.order_by('?')[:count]
        serializer = WordSerializer(words, many=True)
        return Response(serializer.data)


class UserWordViewSet(viewsets.ModelViewSet):
    """ViewSet for UserWord operations."""
    serializer_class = UserWordSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['is_learned', 'review_status']
    ordering = ['-last_reviewed_at']

    def get_queryset(self):
        return UserWord.objects.filter(user=self.request.user).select_related('word')

    def get_serializer_class(self):
        if self.action in ('update', 'partial_update'):
            return UserWordUpdateSerializer
        return UserWordSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def review(self, request, pk=None):
        """Record a review attempt for a user word."""
        user_word = self.get_object()
        is_correct = request.data.get('is_correct', False)

        user_word.times_reviewed += 1
        if is_correct:
            user_word.correct_count += 1
        else:
            user_word.incorrect_count += 1

        user_word.last_reviewed_at = timezone.now()
        # Spaced repetition: next review in 1, 3, 7, 14, 30 days
        intervals = [1, 3, 7, 14, 30]
        interval_index = min(user_word.times_reviewed - 1, len(intervals) - 1)
        user_word.next_review_at = timezone.now() + timedelta(
            days=intervals[interval_index]
        )

        # Update review status
        if user_word.accuracy >= 80 and user_word.times_reviewed >= 5:
            user_word.review_status = UserWord.ReviewStatus.MASTERED
            user_word.is_learned = True
            request.user.total_xp += 3
            request.user.save(update_fields=['total_xp'])
        elif user_word.times_reviewed >= 2:
            user_word.review_status = UserWord.ReviewStatus.REVIEWING
        else:
            user_word.review_status = UserWord.ReviewStatus.LEARNING

        user_word.save()
        return Response(UserWordSerializer(user_word).data)
