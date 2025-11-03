from django.urls import path
from django.contrib.auth import views as auth_views

from . import views


urlpatterns = [
    # u/<username> is top-level

    path('login', views.login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='index'), name='logout'),
    path('change_password', views.change_password, name='change_password'),
    path('preferences', views.preferences, name='preferences'),
]
