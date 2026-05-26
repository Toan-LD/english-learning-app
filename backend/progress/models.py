"""
Models for the progress app.
"""
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from courses.models import Course, Lesson


class UserProgress(models.Model):
    """Model tracking a user's progress in a course."""

    class EnrollmentStatus(models.TextChoices):
        ENROLLED = 'enrolled', _('Enrolled')
        IN_PROGRESS = 'in_progress', _('In Progress')
        COMPLETED = 'completed', _('Completed')
        DROPPED = 'dropped', _('Dropped')

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='user_progresses',
        verbose_name=_('user'),
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='user_progresses',
        verbose_name=_('course'),
    )
    status = models.CharField(
        _('enrollment status'),
        max_length=20,
        choices=EnrollmentStatus.choices,
        default=EnrollmentStatus.ENROLLED,
    )
    completed_lessons = models.ManyToManyField(
        Lesson,
        blank=True,
        related_name='completed_by',
        verbose_name=_('completed lessons'),
    )
    progress_percentage = models.FloatField(
        _('progress percentage'), default=0.0
    )
    total_time_spent = models.PositiveIntegerField(
        _('total time spent (minutes)'), default=0
    )
    enrolled_at = models.DateTimeField(_('enrolled at'), auto_now_add=True)
    last_activity_at = models.DateTimeField(
        _('last activity at'), null=True, blank=True
    )
    completed_at = models.DateTimeField(
        _('completed at'), null=True, blank=True
    )

    class Meta:
        verbose_name = _('user progress')
        verbose_name_plural = _('user progresses')
        unique_together = ['user', 'course']
        ordering = ['-enrolled_at']

    def __str__(self) -> str:
        return f"{self.user.email} - {self.course.title}"

    def update_progress(self):
        """Recalculate progress percentage."""
        total_lessons = self.course.lessons.count()
        if total_lessons == 0:
            self.progress_percentage = 0.0
        else:
            completed = self.completed_lessons.count()
            self.progress_percentage = round(
                (completed / total_lessons) * 100, 1
            )
        self.save(update_fields=['progress_percentage'])


class DailyActivity(models.Model):
    """Model tracking daily learning activity."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='daily_activities',
        verbose_name=_('user'),
    )
    date = models.DateField(_('date'))
    minutes_studied = models.PositiveIntegerField(
        _('minutes studied'), default=0
    )
    words_learned = models.PositiveIntegerField(
        _('words learned'), default=0
    )
    lessons_completed = models.PositiveIntegerField(
        _('lessons completed'), default=0
    )
    quizzes_taken = models.PositiveIntegerField(
        _('quizzes taken'), default=0
    )
    xp_earned = models.PositiveIntegerField(
        _('XP earned'), default=0
    )

    class Meta:
        verbose_name = _('daily activity')
        verbose_name_plural = _('daily activities')
        unique_together = ['user', 'date']
        ordering = ['-date']

    def __str__(self) -> str:
        return f"{self.user.email} - {self.date}"
