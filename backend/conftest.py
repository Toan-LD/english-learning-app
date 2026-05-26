"""
Pytest configuration and fixtures.
"""
import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


@pytest.fixture
def api_client():
    """Return an API client instance."""
    return APIClient()


@pytest.fixture
def user(db):
    """Create and return a test user."""
    return User.objects.create_user(
        email='testuser@example.com',
        username='testuser',
        first_name='Test',
        last_name='User',
        password='TestPass123!',
        learning_level='beginner',
    )


@pytest.fixture
def authenticated_client(api_client, user):
    """Return an authenticated API client."""
    refresh = RefreshToken.for_user(user)
    api_client.credentials(
        HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}'
    )
    return api_client


@pytest.fixture
def admin_user(db):
    """Create and return an admin user."""
    return User.objects.create_superuser(
        email='admin@example.com',
        username='admin',
        first_name='Admin',
        last_name='User',
        password='AdminPass123!',
    )


@pytest.fixture
def sample_word(db):
    """Create a sample word."""
    from vocabulary.models import Word
    return Word.objects.create(
        word='hello',
        phonetic='/həˈloʊ/',
        part_of_speech='noun',
        definition='Used as a greeting.',
        definition_vi='Dùng để chào hỏi.',
        example_sentence='Hello, how are you?',
        difficulty='basic',
    )


@pytest.fixture
def sample_course(db):
    """Create a sample course."""
    from courses.models import Course
    return Course.objects.create(
        title='Test Course',
        slug='test-course',
        description='A test course for unit testing.',
        difficulty='beginner',
        estimated_hours=5.0,
        total_lessons=2,
    )


@pytest.fixture
def sample_lesson(db, sample_course):
    """Create a sample lesson."""
    from courses.models import Lesson
    return Lesson.objects.create(
        course=sample_course,
        title='Test Lesson',
        slug='test-lesson',
        content='<p>Test lesson content.</p>',
        lesson_type='reading',
        order=1,
        duration_minutes=15,
    )


@pytest.fixture
def sample_quiz(db, sample_word):
    """Create a sample quiz."""
    from quiz.models import Quiz, Question
    quiz = Quiz.objects.create(
        title='Test Quiz',
        description='A test quiz.',
        quiz_type='multiple_choice',
        time_limit=300,
        passing_score=70,
    )
    Question.objects.create(
        quiz=quiz,
        word=sample_word,
        question_text="What does 'hello' mean?",
        question_type='multiple_choice',
        correct_answer='Used as a greeting.',
        options=[
            'Used as a greeting.',
            'A type of food.',
            'A place name.',
            'An animal.',
        ],
        points=1,
        order=1,
    )
    return quiz
