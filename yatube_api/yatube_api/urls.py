from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include("api.urls")),
    path("api-token-auth/", obtain_auth_token),
    path(
        "redoc/", TemplateView.as_view(template_name="redoc.html"),
        name="redoc"
    ),
]
