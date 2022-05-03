from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .models import Recipe
from .serializers import RecipeListSerializer, RecipeSerializer


class RecipeListView(APIView):
    """
        Shows all recipies
        TODO: i should add catching with redis in this view
    """
    def get(self, request):
        recipies = Recipe.active.all()
        res = RecipeListSerializer(recipies, many=True)

        return Response(res.data, status=status.HTTP_200_OK)


class RecipeDetailView(APIView):
    """
        Returns all related detail to recipe
        TODO: use catching
    """
    def get(self, request, id, slug):
        recipe = Recipe.active.get(id=id, slug=slug)

        print(recipe)

        res = RecipeSerializer(recipe, many=False)

        return Response(res.data, status=status.HTTP_200_OK)