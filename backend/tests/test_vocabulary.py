"""
Tests for the vocabulary app.
"""
import pytest
from rest_framework import status
from vocabulary.models import Word, UserWord


@pytest.mark.django_db
class TestWordViewSet:
    """Tests for Word CRUD operations."""

    def test_list_words(self, authenticated_client, sample_word):
        """Test listing words."""
        response = authenticated_client.get('/api/vocabulary/words/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] >= 1

    def test_retrieve_word(self, authenticated_client, sample_word):
        """Test retrieving a single word."""
        response = authenticated_client.get(f'/api/vocabulary/words/{sample_word.id}/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['word'] == 'hello'

    def test_search_words(self, authenticated_client, sample_word):
        """Test searching words."""
        response = authenticated_client.get('/api/vocabulary/words/?search=hello')
        assert response.status_code == status.HTTP_200_OK

    def test_mark_word_learned(self, authenticated_client, sample_word):
        """Test marking a word as learned."""
        response = authenticated_client.post(
            f'/api/vocabulary/words/{sample_word.id}/mark_learned/'
        )
        assert response.status_code == status.HTTP_200_OK
        assert UserWord.objects.filter(
            word=sample_word, is_learned=True
        ).exists()

    def test_random_words(self, authenticated_client, sample_word):
        """Test getting random words."""
        response = authenticated_client.get('/api/vocabulary/words/random/?count=5')
        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestUserWordViewSet:
    """Tests for UserWord operations."""

    def test_list_user_words(self, authenticated_client, user, sample_word):
        """Test listing user words."""
        UserWord.objects.create(user=user, word=sample_word)
        response = authenticated_client.get('/api/vocabulary/user-words/')
        assert response.status_code == status.HTTP_200_OK

    def test_review_word(self, authenticated_client, user, sample_word):
        """Test reviewing a word."""
        user_word = UserWord.objects.create(user=user, word=sample_word)
        response = authenticated_client.post(
            f'/api/vocabulary/user-words/{user_word.id}/review/',
            {'is_correct': True},
        )
        assert response.status_code == status.HTTP_200_OK
        user_word.refresh_from_db()
        assert user_word.times_reviewed == 1
        assert user_word.correct_count == 1


@pytest.mark.django_db
class TestWordModel:
    """Tests for Word model."""

    def test_word_str(self, sample_word):
        """Test word string representation."""
        assert str(sample_word) == 'hello'

    def test_user_word_accuracy(self, user, sample_word):
        """Test UserWord accuracy calculation."""
        user_word = UserWord.objects.create(
            user=user, word=sample_word,
            correct_count=8, incorrect_count=2,
        )
        assert user_word.accuracy == 80.0
