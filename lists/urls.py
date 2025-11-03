from django.urls import path

from . import views

urlpatterns = [
    path('create', views.create_list, name='create_list'),
    path('<int:listid>/', views.list_dash, name='list_dash'),
    path('<int:listid>/delete/<int:rowid>/', views.delete_row, name='delete_row'),
]
