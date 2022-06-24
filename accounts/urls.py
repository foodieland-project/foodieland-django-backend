from django.urls import path
from . import views


app_name = "accounts"

urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create'),
]