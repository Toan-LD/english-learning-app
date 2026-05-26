"""
Models for the vocabulary app.
"""
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class Word(models.Model):
    """Word model representing an English vocabulary word."""

    class PartOfSpeech(models.TextChoices):
        NOUN = 'noun', _('Noun')
        VERB = 'verb', _('Verb')
        ADJECTIVE = 'adjective', _('Adjective')
        ADVERB = 'adverb', _('Adverb')
        PRONOUN = 'pronoun', _('Pronoun')
        PREPOSITION = 'preposition', _('Preposition')
        CONJUNCTION = 'conjunction', _('Conjunction')
        INTERJECTION = 'interjection', _('Interjection')

    class DifficultyLevel(models.TextChoices):
        BASIC = 'basic', _('Basic')
        INTERMEDIATE = 'intermediate', _('Intermediate')
        ADVANCED = 'advanced', _('Advanced')

    word = models.CharField(_('word'), max_length=100, unique=True)
    phonetic = models.CharField(
        _('phonetic transcription'), max_length=100, blank=True, default=''
    )
    part_of_speech = models.CharField(
        _('part of speech'),
        max_length=20,
        choices=PartOfSpeech.choices,
        default=PartOfSpeech.NOUN,
    )
    definition = models.TextField(_('definition'))
    example_sentence = models.TextField(
        _('example sentence'), blank=True, default=''
    )
    example_sentence_vi = models.TextField(
        _('example sentence (Vietnamese)'), blank=True, default=''
    )
    definition_vi = models.TextField(
        _('definition (Vietnamese)'), blank=True, default=''
    )
    synonym = models.CharField(
        _('synonyms'), max_length=500, blank=True, default=''
    )
    antonym = models.CharField(
        _('antonyms'), max_length=500, blank=True, default=''
    )
    difficulty = models.CharField(
        _('difficulty'),
        max_length=20,
        choices=DifficultyLevel.choices,
        default=DifficultyLevel.BASIC,
    )
    image = models.ImageField(
        _('image'), upload_to='words/images/', blank=True, null=True
    )
    audio_url = models.URLField(_('audio URL'), blank=True, default='')
    is_active = models.BooleanField(_('is active'), default=True)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    class Meta:
        verbose_name = _('word')
        verbose_name_plural = _('words')
        ordering = ['word']

    def __str__(self) -> str:
        return self.word


class UserWord(models.Model):
    """Model tracking a user's relationship with a word."""

    class ReviewStatus(models.TextChoices):
        NEW = 'new', _('New')
        LEARNING = 'learning', _('Learning')
        REVIEWING = 'reviewing', _('Reviewing')
        MASTERED = 'mastered', _('Mastered')

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='user_words',
        verbose_name=_('user'),
    )
    word = models.ForeignKey(
        Word,
        on_delete=models.CASCADE,
        related_name='user_words',
        verbose_name=_('word'),
    )
    is_learned = models.BooleanField(_('is learned'), default=False)
    review_status = models.CharField(
        _('review status'),
        max_length=20,
        choices=ReviewStatus.choices,
        default=ReviewStatus.NEW,
    )
    times_reviewed = models.PositiveIntegerField(
        _('times reviewed'), default=0
    )
    correct_count = models.PositiveIntegerField(
        _('correct count'), default=0
    )
    incorrect_count = models.PositiveIntegerField(
        _('incorrect count'), default=0
    )
    last_reviewed_at = models.DateTimeField(
        _('last reviewed at'), null=True, blank=True
    )
    next_review_at = models.DateTimeField(
        _('next review at'), null=True, blank=True
    )
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    class Meta:
        verbose_name = _('user word')
        verbose_name_plural = _('user words')
        unique_together = ['user', 'word']
        ordering = ['-last_reviewed_at']

    def __str__(self) -> str:
        return f"{self.user.email} - {self.word.word}"

    @property
    def accuracy(self) -> float:
        """Calculate accuracy percentage."""
        total = self.correct_count + self.incorrect_count
        if total == 0:
            return 0.0
        return round((self.correct_count / total) * 100, 1)
