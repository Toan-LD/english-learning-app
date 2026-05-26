"""
Models for the courses app.
"""
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class Course(models.Model):
    """Course model representing a learning course."""

    class Difficulty(models.TextChoices):
        BEGINNER = 'beginner', _('Beginner')
        INTERMEDIATE = 'intermediate', _('Intermediate')
        ADVANCED = 'advanced', _('Advanced')

    title = models.CharField(_('title'), max_length=200)
    slug = models.SlugField(_('slug'), max_length=200, unique=True)
    description = models.TextField(_('description'))
    thumbnail = models.ImageField(
        _('thumbnail'), upload_to='courses/thumbnails/', blank=True, null=True
    )
    difficulty = models.CharField(
        _('difficulty'),
        max_length=20,
        choices=Difficulty.choices,
        default=Difficulty.BEGINNER,
    )
    is_published = models.BooleanField(_('is published'), default=True)
    total_lessons = models.PositiveIntegerField(
        _('total lessons'), default=0
    )
    estimated_hours = models.DecimalField(
        _('estimated hours'),
        max_digits=4,
        decimal_places=1,
        default=0.0,
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='created_courses',
        verbose_name=_('created by'),
        null=True,
    )
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    class Meta:
        verbose_name = _('course')
        verbose_name_plural = _('courses')
        ordering = ['created_at']

    def __str__(self) -> str:
        return self.title

    @property
    def lesson_count(self) -> int:
        """Return actual lesson count."""
        return self.lessons.count()


class Lesson(models.Model):
    """Lesson model belonging to a course."""

    class LessonType(models.TextChoices):
        VIDEO = 'video', _('Video')
        READING = 'reading', _('Reading')
        QUIZ = 'quiz', _('Quiz')
        PRACTICE = 'practice', _('Practice')

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='lessons',
        verbose_name=_('course'),
    )
    title = models.CharField(_('title'), max_length=200)
    slug = models.SlugField(_('slug'), max_length=200)
    content = models.TextField(_('content'))
    lesson_type = models.CharField(
        _('lesson type'),
        max_length=20,
        choices=LessonType.choices,
        default=LessonType.READING,
    )
    order = models.PositiveIntegerField(_('order'), default=0)
    duration_minutes = models.PositiveIntegerField(
        _('duration (minutes)'), default=15
    )
    video_url = models.URLField(_('video URL'), blank=True, default='')
    is_free = models.BooleanField(_('is free'), default=False)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    class Meta:
        verbose_name = _('lesson')
        verbose_name_plural = _('lessons')
        ordering = ['course', 'order']
        unique_together = ['course', 'slug']

    def __str__(self) -> str:
        return f"{self.course.title} - {self.title}"
