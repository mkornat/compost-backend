"""compost_backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework_simplejwt.views import TokenRefreshView

from users.views import SignInView, TokenObtainPairView

import compost.urls

auth_patterns = [
    path("sign-in/", SignInView.as_view(), name="sign_in_view"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]

api_patterns = [
    path("auth/", include((auth_patterns, "auth"))),
    path("compost/", include((compost.urls, "compost"))),
]

api_schema_view = get_schema_view(
    openapi.Info(
        title="SMOK",
        description="System Monitoringu Osobistych Kompostowników",
        default_version="0.1.0",
    ),
    patterns=api_patterns,
    public=True,
)

urlpatterns = api_patterns + [
    path(
        "swagger/",
        api_schema_view.with_ui("swagger", cache_timeout=0),
        name="api-schema-swagger-ui",
    ),
    path("admin/", admin.site.urls),
]
