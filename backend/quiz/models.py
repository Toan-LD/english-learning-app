"""
Models for the quiz app.
"""
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from vocabulary.models import Word
from courses.models import Lesson


class Quiz(models.Model):
    """Quiz model representing a vocabulary quiz."""

    class QuizType(models.TextChoices):
        MULTIPLE_CHOICE = 'multiple_choice', _('Multiple Choice')
        FILL_IN_BLANK = 'fill_in_blank', _('Fill in the Blank')
        MATCHING = 'matching', _('Matching')
        LISTENING = 'listening', _('Listening')

    title = models.CharField(_('title'), max_length=200)
    description = models.TextField(_('description'), blank=True, default='')
    quiz_type = models.CharField(
        _('quiz type'),
        max_length=20,
        choices=QuizType.choices,
        default=QuizType.MULTIPLE_CHOICE,
    )
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name='quizzes',
        verbose_name=_('lesson'),
        null=True,
        blank=True,
    )
    time_limit = models.PositiveIntegerField(
        _('time limit (seconds)'),
        default=300,
        help_text=_('Time limit in seconds, 0 for unlimited'),
    )
    passing_score = models.PositiveIntegerField(
        _('passing score (%)'), default=70
    )
    is_active = models.BooleanField(_('is active'), default=True)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    class Meta:
        verbose_name = _('quiz')
        verbose_name_plural = _('quizzes')
        ordering = ['-created_at']

    def __str__(self) -> str:
        return self.title

    @property
    def question_count(self) -> int:
        return self.questions.count()


class Question(models.Model):
    """Question model belonging to a quiz."""
    quiz = models.ForeignKey(
        Quiz,
        on_delete=models.CASCADE,
        related_name='questions',
        verbose_name=_('quiz'),
    )
    word = models.ForeignKey(
        Word,
        on_delete=models.CASCADE,
        related_name='questions',
        verbose_name=_('word'),
        null=True,
        blank=True,
    )
    question_text = models.TextField(_('question text'))
    question_type = models.CharField(
        _('question type'),
        max_length=20,
        choices=Quiz.QuizType.choices,
        default=Quiz.QuizType.MULTIPLE_CHOICE,
    )
    correct_answer = models.CharField(_('correct answer'), max_length=500)
    options = models.JSONField(
        _('options'),
        default=list,
        help_text=_('List of answer options for multiple choice'),
    )
    points = models.PositiveIntegerField(_('points'), default=1)
    order = models.PositiveIntegerField(_('order'), default=0)
    explanation = models.TextField(_('explanation'), blank=True, default='')

    class Meta:
        verbose_name = _('question')
        verbose_name_plural = _('questions')
        ordering = ['quiz', 'order']

    def __str__(self) -> str:
        return f"{self.quiz.title} - Q{self.order}: {self.question_text[:50]}"


class QuizAttempt(models.Model):
    """Model tracking a user's quiz attempt."""

    class Status(models.TextChoices):
        IN_PROGRESS = 'in_progress', _('In Progress')
        COMPLETED = 'completed', _('Completed')
        ABANDONED = 'abandoned', _('Abandoned')

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='quiz_attempts',
        verbose_name=_('user'),
    )
    quiz = models.ForeignKey(
        Quiz,
        on_delete=models.CASCADE,
        related_name='attempts',
        verbose_name=_('quiz'),
    )
    score = models.FloatField(_('score'), default=0)
    total_questions = models.PositiveIntegerField(
        _('total questions'), default=0
    )
    correct_answers = models.PositiveIntegerField(
        _('correct answers'), default=0
    )
    time_taken = models.PositiveIntegerField(
        _('time taken (seconds)'), default=0
    )
    status = models.CharField(
        _('status'),
        max_length=20,
        choices=Status.choices,
        default=Status.IN_PROGRESS,
    )
    answers = models.JSONField(
        _('answers'),
        default=dict,
        help_text=_('Dictionary of question_id: user_answer'),
    )
    started_at = models.DateTimeField(_('started at'), auto_now_add=True)
    completed_at = models.DateTimeField(
        _('completed at'), null=True, blank=True
    )

    class Meta:
        verbose_name = _('quiz attempt')
        verbose_name_plural = _('quiz attempts')
        ordering = ['-started_at']

    def __str__(self) -> str:
        return f"{self.user.email} - {self.quiz.title} ({self.score}%)"

    @property
    def percentage(self) -> float:
        if self.total_questions == 0:
            return 0.0
        return round((self.correct_answers / self.total_questions) * 100, 1)
