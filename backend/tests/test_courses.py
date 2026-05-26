"""
Tests for the courses app.
"""
import pytest
from rest_framework import status
from courses.models import Course, Lesson


@pytest.mark.django_db
class TestCourseViewSet:
    """Tests for Course CRUD operations."""

    def test_list_courses(self, authenticated_client, sample_course):
        """Test listing courses."""
        response = authenticated_client.get('/api/courses/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] >= 1

    def test_retrieve_course(self, authenticated_client, sample_course):
        """Test retrieving a single course."""
        response = authenticated_client.get(f'/api/courses/{sample_course.slug}/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == sample_course.title

    def test_create_course(self, authenticated_client):
        """Test creating a new course."""
        data = {
            'title': 'New Course',
            'slug': 'new-course',
            'description': 'A brand new course.',
            'difficulty': 'intermediate',
            'estimated_hours': 8.0,
        }
        response = authenticated_client.post('/api/courses/', data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['title'] == 'New Course'

    def test_search_courses(self, authenticated_client, sample_course):
        """Test searching courses."""
        response = authenticated_client.get('/api/courses/?search=Test')
        assert response.status_code == status.HTTP_200_OK

    def test_unpublished_courses_hidden(self, authenticated_client):
        """Test that unpublished courses are not listed."""
        Course.objects.create(
            title='Hidden Course',
            slug='hidden-course',
            description='Not visible.',
            is_published=False,
        )
        response = authenticated_client.get('/api/courses/')
        titles = [c['title'] for c in response.data['results']]
        assert 'Hidden Course' not in titles


@pytest.mark.django_db
class TestLessonViewSet:
    """Tests for Lesson CRUD operations."""

    def test_list_lessons(self, authenticated_client, sample_lesson):
        """Test listing lessons."""
        response = authenticated_client.get('/api/courses/lessons/')
        assert response.status_code == status.HTTP_200_OK

    def test_retrieve_lesson(self, authenticated_client, sample_lesson):
        """Test retrieving a single lesson."""
        response = authenticated_client.get(f'/api/courses/lessons/{sample_lesson.id}/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == 'Test Lesson'


@pytest.mark.django_db
class TestCourseModel:
    """Tests for Course model."""

    def test_course_str(self, sample_course):
        """Test course string representation."""
        assert str(sample_course) == 'Test Course'

    def test_lesson_count(self, sample_course, sample_lesson):
        """Test lesson count property."""
        assert sample_course.lesson_count == 1
