"""
URL configuration for minddistrict project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path

import dlo_client.views as dlo_views

urlpatterns = [
    path("", dlo_views.index, name="index"),
    path("admin/", admin.site.urls),
    path(
        "redirect_to_professional_account/",
        dlo_views.redirect_to_professional_account,
        name="redirect_to_professional_account",
    ),
    path(
        "redirect_to_client_account/",
        dlo_views.redirect_to_client_account,
        name="redirect_to_client_account",
    ),
    path(
        "redirect_to_professional_account_with_redirect_target/",
        dlo_views.redirect_to_professional_account_with_redirect_target,
        name="redirect_to_professional_account_with_redirect_target",
    ),
    path(
        "redirect_to_client_account_with_redirect_target/",
        dlo_views.redirect_to_client_account_with_redirect_target,
        name="redirect_to_client_account_with_redirect_target",
    ),
]
