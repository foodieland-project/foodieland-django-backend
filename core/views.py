from django.shortcuts import get_object_or_404, render
from django.contrib.auth import get_user_model
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
# from utilities.pagination import PaginationHandlerMixin
# from utilities.permissions import IsOwnerOrReadOnly, IsSuperUserMixin, ReadOnly
from django.http import HttpResponse
from django.shortcuts import render
from .models import Comment

from rest_framework.permissions import IsAuthenticated, AllowAny
from utilities.permissions import IsOwnerOrReadOnly, IsSuperUserMixin, ReadOnly


# getting the User model based on setting that we defined in settings.py
User = get_user_model()



