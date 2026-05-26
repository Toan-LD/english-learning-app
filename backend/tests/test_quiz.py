"""
Tests for the quiz app.
"""
import pytest
from rest_framework import status
from quiz.models import Quiz, QuizAttempt


@pytest.mark.django_db
class TestQuizViewSet:
    """Tests for Quiz operations."""

    def test_list_quizzes(self, authenticated_client, sample_quiz):
        """Test listing quizzes."""
        response = authenticated_client.get('/api/quiz/')
        assert response.status_code == status.HTTP_200_OK

    def test_retrieve_quiz(self, authenticated_client, sample_quiz):
        """Test retrieving a single quiz."""
        response = authenticated_client.get(f'/api/quiz/{sample_quiz.id}/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == 'Test Quiz'
        # Ensure correct_answer is hidden
        for q in response.data.get('questions', []):
            assert 'correct_answer' not in q

    def test_start_quiz(self, authenticated_client, sample_quiz):
        """Test starting a quiz attempt."""
        response = authenticated_client.post(f'/api/quiz/{sample_quiz.id}/start/')
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['status'] == 'in_progress'

    def test_submit_quiz(self, authenticated_client, sample_quiz):
        """Test submitting quiz answers."""
        question = sample_quiz.questions.first()
        # Start first
        authenticated_client.post(f'/api/quiz/{sample_quiz.id}/start/')

        data = {
            'answers': {str(question.id): 'Used as a greeting.'},
            'time_taken': 120,
        }
        response = authenticated_client.post(
            f'/api/quiz/{sample_quiz.id}/submit/',
            data,
            format='json',
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.data['correct_answers'] == 1
        assert response.data['score'] == 100.0
        assert response.data['passed'] is True

    def test_submit_wrong_answer(self, authenticated_client, sample_quiz):
        """Test submitting wrong answers."""
        question = sample_quiz.questions.first()
        authenticated_client.post(f'/api/quiz/{sample_quiz.id}/start/')

        data = {
            'answers': {str(question.id): 'A type of food.'},
            'time_taken': 60,
        }
        response = authenticated_client.post(
            f'/api/quiz/{sample_quiz.id}/submit/',
            data,
            format='json',
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.data['correct_answers'] == 0


@pytest.mark.django_db
class TestQuizModel:
    """Tests for Quiz model."""

    def test_quiz_str(self, sample_quiz):
        """Test quiz string representation."""
        assert str(sample_quiz) == 'Test Quiz'

    def test_question_count(self, sample_quiz):
        """Test question count property."""
        assert sample_quiz.question_count == 1
