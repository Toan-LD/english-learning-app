"""
Views for the users app.
"""
from django.contrib.auth import get_user_model
from django.db import models
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import (
    UserRegistrationSerializer,
    UserSerializer,
    UserUpdateSerializer,
    ChangePasswordSerializer,
    CustomTokenObtainPairSerializer,
)

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    """API endpoint for user registration."""
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': UserSerializer(user).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }, status=status.HTTP_201_CREATED)


class LoginView(TokenObtainPairView):
    """API endpoint for user login with JWT tokens."""
    serializer_class = CustomTokenObtainPairSerializer
    permission_classes = [permissions.AllowAny]


class LogoutView(APIView):
    """API endpoint for user logout (blacklist refresh token)."""

    def post(self, request) -> Response:
        try:
            refresh_token = request.data.get('refresh')
            if not refresh_token:
                return Response(
                    {'error': 'Refresh token is required.'},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(
                {'message': 'Successfully logged out.'},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {'error': f'Invalid token: {str(e)}'},
                status=status.HTTP_400_BAD_REQUEST,
            )


class ProfileView(generics.RetrieveUpdateAPIView):
    """API endpoint for viewing and updating user profile."""
    serializer_class = UserSerializer

    def get_object(self) -> User:
        return self.request.user

    def get_serializer_class(self):
        if self.request.method in ('PUT', 'PATCH'):
            return UserUpdateSerializer
        return UserSerializer


class ChangePasswordView(APIView):
    """API endpoint for changing user password."""

    def post(self, request) -> Response:
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user
        if not user.check_password(serializer.validated_data['old_password']):
            return Response(
                {'old_password': 'Wrong password.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user.set_password(serializer.validated_data['new_password'])
        user.save()
        return Response(
            {'message': 'Password changed successfully.'},
            status=status.HTTP_200_OK,
        )


class UserStatsView(APIView):
    """API endpoint for user statistics."""

    def get(self, request) -> Response:
        user = request.user
        from progress.models import UserProgress
        from vocabulary.models import UserWord
        from quiz.models import QuizAttempt

        total_words_learned = UserWord.objects.filter(
            user=user, is_learned=True
        ).count()
        total_courses = UserProgress.objects.filter(user=user).count()
        total_quizzes = QuizAttempt.objects.filter(user=user).count()
        avg_quiz_score = QuizAttempt.objects.filter(
            user=user
        ).aggregate(avg=models.Avg('score'))['avg'] or 0

        return Response({
            'total_xp': user.total_xp,
            'streak_days': user.streak_days,
            'total_words_learned': total_words_learned,
            'total_courses_enrolled': total_courses,
            'total_quizzes_taken': total_quizzes,
            'average_quiz_score': round(float(avg_quiz_score), 1),
            'daily_goal': user.daily_goal,
            'learning_level': user.learning_level,
        })
