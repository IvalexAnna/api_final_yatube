from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView, TokenVerifyView)
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api-token-auth/", obtain_auth_token),
    path(
        "api/v1/jwt/create/", TokenObtainPairView.as_view(), name="token_obtain_pair"
    ),  # Получение JWT-токена
    path(
        "api/v1/jwt/refresh/", TokenRefreshView.as_view(), name="token_refresh"
    ),  # Обновление JWT-токена
    path(
        "api/v1/jwt/verify/", TokenVerifyView.as_view(), name="token_verify"
    ),  # Проверка JWT-токена
    path("api/v1/", include("api.urls")),  # Подключение маршрутов API
    path(
        "redoc/", TemplateView.as_view(template_name="redoc.html"), name="redoc"
    ),  # Документация API
]
