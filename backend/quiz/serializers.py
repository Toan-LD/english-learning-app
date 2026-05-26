"""
Serializers for the quiz app.
"""
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from .models import Quiz, Question, QuizAttempt


class QuestionSerializer(serializers.ModelSerializer):
    """Serializer for Question model."""

    class Meta:
        model = Question
        fields = [
            'id', 'quiz', 'word', 'question_text', 'question_type',
            'correct_answer', 'options', 'points', 'order',
            'explanation',
        ]
        read_only_fields = ['id']

    def to_representation(self, instance):
        """Hide correct answer when serving to users."""
        data = super().to_representation(instance)
        if not self.context.get('show_answers', False):
            data.pop('correct_answer', None)
            data.pop('explanation', None)
        return data


class QuestionWithAnswerSerializer(serializers.ModelSerializer):
    """Serializer for Question with correct answers shown."""

    class Meta:
        model = Question
        fields = [
            'id', 'quiz', 'word', 'question_text', 'question_type',
            'correct_answer', 'options', 'points', 'order',
            'explanation',
        ]


class QuizSerializer(serializers.ModelSerializer):
    """Serializer for Quiz model."""
    questions = QuestionSerializer(many=True, read_only=True)
    question_count = serializers.ReadOnlyField()

    class Meta:
        model = Quiz
        fields = [
            'id', 'title', 'description', 'quiz_type', 'lesson',
            'time_limit', 'passing_score', 'is_active',
            'question_count', 'questions',
            'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class QuizListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for quiz listing."""
    question_count = serializers.ReadOnlyField()

    class Meta:
        model = Quiz
        fields = [
            'id', 'title', 'description', 'quiz_type',
            'time_limit', 'passing_score', 'question_count',
            'created_at',
        ]


class QuizAttemptSerializer(serializers.ModelSerializer):
    """Serializer for QuizAttempt model."""
    quiz_title = serializers.CharField(source='quiz.title', read_only=True)
    percentage = serializers.ReadOnlyField()

    class Meta:
        model = QuizAttempt
        fields = [
            'id', 'user', 'quiz', 'quiz_title', 'score',
            'total_questions', 'correct_answers', 'time_taken',
            'status', 'answers', 'percentage',
            'started_at', 'completed_at',
        ]
        read_only_fields = [
            'id', 'user', 'score', 'correct_answers',
            'started_at', 'completed_at',
        ]


class QuizSubmitSerializer(serializers.Serializer):
    """Serializer for submitting quiz answers."""
    answers = serializers.DictField(
        child=serializers.CharField(),
        help_text=_('Dictionary of question_id: user_answer'),
    )
    time_taken = serializers.IntegerField(
        help_text=_('Time taken in seconds'),
    )
