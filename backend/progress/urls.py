"""
URL patterns for the progress app.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'stats', views.ProgressStatsView, basename='progress-stats')
router.register(r'activities', views.DailyActivityViewSet, basename='daily-activity')
router.register(r'', views.UserProgressViewSet, basename='user-progress')

urlpatterns = [
    path('', include(router.urls)),
]
