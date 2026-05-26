"""
Custom User model for the English Learning Platform.
"""
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """Custom user model with additional fields for learning platform."""

    class LearningLevel(models.TextChoices):
        BEGINNER = 'beginner', _('Beginner')
        INTERMEDIATE = 'intermediate', _('Intermediate')
        ADVANCED = 'advanced', _('Advanced')
        PROFICIENT = 'proficient', _('Proficient')

    email = models.EmailField(_('email address'), unique=True)
    bio = models.TextField(_('bio'), blank=True, default='')
    avatar = models.ImageField(
        _('avatar'), upload_to='avatars/', blank=True, null=True
    )
    learning_level = models.CharField(
        _('learning level'),
        max_length=20,
        choices=LearningLevel.choices,
        default=LearningLevel.BEGINNER,
    )
    daily_goal = models.PositiveIntegerField(
        _('daily goal (minutes)'),
        default=30,
        help_text=_('Daily learning goal in minutes'),
    )
    streak_days = models.PositiveIntegerField(
        _('streak days'),
        default=0,
        help_text=_('Consecutive days of learning'),
    )
    last_active_date = models.DateField(
        _('last active date'),
        null=True,
        blank=True,
    )
    total_xp = models.PositiveIntegerField(
        _('total experience points'),
        default=0,
    )
    is_notification_enabled = models.BooleanField(
        _('notification enabled'),
        default=True,
    )
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        ordering = ['-created_at']

    def __str__(self) -> str:
        return self.email

    @property
    def full_name(self) -> str:
        """Return the user's full name."""
        return f"{self.first_name} {self.last_name}".strip()

    @property
    def words_learned(self) -> int:
        """Return the count of words the user has learned."""
        return self.user_words.filter(is_learned=True).count()

    @property
    def courses_enrolled(self) -> int:
        """Return the count of courses the user is enrolled in."""
        return self.user_progresses.count()
