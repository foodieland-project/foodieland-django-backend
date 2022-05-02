from django.urls import path
from . import views

app_name = 'recipe'
urlpatterns = [
    path('recipe_list/', views.RecipeListView.as_view(), name='recipe_list')
]