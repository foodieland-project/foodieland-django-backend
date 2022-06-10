from django.urls import path, include
from rest_framework import routers
from . import views

app_name = 'blog'
urlpatterns = [
    path('articles/', views.ArticleListView.as_view(), name="articles"),
    path('article/detail/<pk>/<str:slug>/', views.ArticleDetail.as_view(), name="article_detail")
]

