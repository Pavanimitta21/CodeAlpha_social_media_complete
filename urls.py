
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/register/', views.api_register, name='api_register'),
    path('api/login/', views.api_login, name='api_login'),
    path('api/logout/', views.api_logout, name='api_logout'),
    path('api/posts/', views.api_create_post, name='api_create_post'),
    path('api/feed/', views.api_feed, name='api_feed'),
    path('api/posts/<int:post_id>/comments/', views.api_comment, name='api_comment'),
    path('api/posts/<int:post_id>/like/', views.api_like, name='api_like'),
]
