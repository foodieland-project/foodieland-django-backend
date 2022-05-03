from django.urls import path
from . import views

app_name = 'recipe'
urlpatterns = [
    path('recipe_list/', views.RecipeListView.as_view(), name='recipe_list'),
    path('recipe_detail/<int:id>/<str:slug>', views.RecipeDetailView.as_view(), name='recipe_detail'),
]