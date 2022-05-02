from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .models import Recipe
from .serializers import RecipeSerializer


class RecipeListView(APIView):
    """
        Shows all recipies
        TODO: i should add catching with redis in this view
    """
    def get(self, request):
        recipies = Recipe.active.all()
        response = RecipeSerializer(recipies, many=True)

        return Response(response.data, status=status.HTTP_200_OK)


