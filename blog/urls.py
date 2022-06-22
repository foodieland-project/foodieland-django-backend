from django.urls import path, include
from rest_framework import routers
from . import views

app_name = 'blog'
urlpatterns = [
    # articles
    path('articles/', views.ArticleListView.as_view(), name="articles"),
    path('article/detail/<pk>/<str:slug>/',
         views.ArticleDetail.as_view(), name="article_detail"),

    # article-by-category
    path('article/category/<str:category>/',
         views.ArticleCategory.as_view(), name="article_by_category"),

    # category
    path('category/', views.CategoryListView.as_view(), name="category_list")
]
