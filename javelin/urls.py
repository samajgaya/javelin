"""
URL configuration for javelin project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path, include

from django.contrib.auth import views as auth_views
from core import views as core_views
from accounts import views as account_views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('u/<str:username>/', account_views.profile, name='profile'),
    path('login', account_views.login, name='login'),
    path('preferences', account_views.preferences, name='preferences'),
    path('logout', auth_views.LogoutView.as_view(next_page='index'), name='logout'),

    path('l/', include('lists.urls')),

    path('', core_views.index, name='index')
]
