"""actnow URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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

from .summary import summary
from .token import TokenView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("v1/accounts/", include("actnow.accounts.urls")),
    path("v1/", summary, name="summary"),
    path("v1/petitions/", include("actnow.petitions.urls")),
    path("v1/profiles/", include("actnow.profiles.urls")),
    path("o/token/", TokenView.as_view(), name="token"),
    path("o/", include("oauth2_provider.urls", namespace="oauth2_provider")),
    path("auth/", include("actnow.social.urls")),
    path("", include("actnow.site.urls")),
]
