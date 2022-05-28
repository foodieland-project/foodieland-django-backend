from django.urls import path, include
from rest_framework import routers
from . import views

app_name = 'blog'
urlpatterns = [
    path('articles/', views.ArticleListView.as_view(), name="articles"),
]

