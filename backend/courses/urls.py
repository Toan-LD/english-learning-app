"""
URL patterns for the courses app.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'lessons', views.LessonViewSet, basename='lesson')
router.register(r'', views.CourseViewSet, basename='course')

urlpatterns = [
    path('', include(router.urls)),
]
