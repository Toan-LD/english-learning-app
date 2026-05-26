"""
URL patterns for the vocabulary app.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'user-words', views.UserWordViewSet, basename='user-word')
router.register(r'words', views.WordViewSet, basename='word')

urlpatterns = [
    path('', include(router.urls)),
]
