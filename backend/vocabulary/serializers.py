"""
Serializers for the vocabulary app.
"""
from rest_framework import serializers
from .models import Word, UserWord


class WordSerializer(serializers.ModelSerializer):
    """Serializer for Word model."""

    class Meta:
        model = Word
        fields = [
            'id', 'word', 'phonetic', 'part_of_speech',
            'definition', 'example_sentence', 'example_sentence_vi',
            'definition_vi', 'synonym', 'antonym', 'difficulty',
            'image', 'audio_url', 'is_active',
            'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class WordListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for word listing."""

    class Meta:
        model = Word
        fields = [
            'id', 'word', 'phonetic', 'part_of_speech',
            'definition', 'difficulty',
        ]


class UserWordSerializer(serializers.ModelSerializer):
    """Serializer for UserWord model."""
    word = WordSerializer(read_only=True)
    word_id = serializers.PrimaryKeyRelatedField(
        queryset=Word.objects.all(), source='word', write_only=True
    )
    accuracy = serializers.ReadOnlyField()

    class Meta:
        model = UserWord
        fields = [
            'id', 'user', 'word', 'word_id', 'is_learned',
            'review_status', 'times_reviewed', 'correct_count',
            'incorrect_count', 'accuracy', 'last_reviewed_at',
            'next_review_at', 'created_at', 'updated_at',
        ]
        read_only_fields = [
            'id', 'user', 'times_reviewed', 'correct_count',
            'incorrect_count', 'last_reviewed_at', 'next_review_at',
            'created_at', 'updated_at',
        ]


class UserWordUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating UserWord status."""

    class Meta:
        model = UserWord
        fields = [
            'is_learned', 'review_status',
            'correct_count', 'incorrect_count',
        ]
