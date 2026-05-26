"""
URL patterns for the quiz app.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'attempts', views.QuizAttemptViewSet, basename='quiz-attempt')
router.register(r'questions', views.QuestionViewSet, basename='question')
router.register(r'', views.QuizViewSet, basename='quiz')

urlpatterns = [
    path('', include(router.urls)),
]
