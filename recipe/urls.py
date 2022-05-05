from django.urls import path
from . import views

app_name = 'recipe'
urlpatterns = [
    # recpies
    path('recipe/', views.RecipeListView.as_view(), name='recipe_list'),
    path('recipe-detail/<int:id>/<str:slug>', views.RecipeDetailView.as_view(), name='recipe_detail'),

    # comments
    path('comments/<int:pk>/', views.CommentListView.as_view(), name="comment-per-recipe"),
    path('comment/create/<int:recipe_id>/', views.CommentCreate.as_view(), name="recipe-create-comment"),
    path('comment/update/<int:recipe_id>/<int:comment_id>/', views.CommentUpdate.as_view(), name="recipe-update-comment"),
    path('comment/delete/<int:recipe_id>/<int:comment_id>/', views.CommentDelete.as_view(), name="recipe-delete-comment"),

    # replies
    path('reply/create/<int:recipe_id>/<int:comment_id>/', views.ReplyCreate.as_view(), name="reply-create"),
    path('reply/update/<int:recipe_id>/<int:comment_id>/<int:reply_id>/', views.ReplyUpdate.as_view(), name="reply-update"),
    path('reply/delete/<int:recipe_id>/<int:comment_id>/<int:reply_id>/', views.ReplyDelete.as_view(), name="reply-delete"),
    path('reply/<int:pk>/', views.ReplyListView.as_view(), name="comment-replies"),
]