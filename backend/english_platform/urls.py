"""
URL configuration for english_platform project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="English Learning Platform API",
        default_version='v1',
        description="Complete API for English Learning Platform",
        terms_of_service="https://www.english-platform.com/terms/",
        contact=openapi.Contact(email="admin@english-platform.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),
    path('api/courses/', include('courses.urls')),
    path('api/vocabulary/', include('vocabulary.urls')),
    path('api/quiz/', include('quiz.urls')),
    path('api/progress/', include('progress.urls')),
    # Swagger documentation
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0),
         name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0),
         name='schema-redoc'),
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0),
         name='schema-json'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

admin.site.site_header = "English Learning Platform Admin"
admin.site.site_title = "English Platform Admin"
admin.site.index_title = "Welcome to English Learning Platform"
