from rest_framework.response import Response
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView
from rest_framework.views import  APIView
from django.shortcuts import get_object_or_404
from .models import Article, Category
from .serializers import ArticleSerializer, CategorySerializer
from utilities.permissions import IsStaffOrReadOnly, IsSuperUserMixin


# TODO: Use get_object_or_404

class ArticleListView(ListAPIView):
    """
        Shows all articles that are active (by is_active)
    """
    queryset = Article.objects.filter(is_active=True)
    serializer_class = ArticleSerializer


class ArticleDetail(RetrieveUpdateDestroyAPIView):
    queryset = Article.objects.filter(is_active=True)
    serializer_class = ArticleSerializer


class CategoryViewSet(ListAPIView):
    """
    Showing all categries
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ArticleCategory(APIView):
    """
    This view will filter and show
    the articles by their category
    """

    def get(self, request, category):
        # getting the category name
        category = self.kwargs['category']
        category_model = get_object_or_404(Category, slug=category)
    
        # filtering article by category
        article = Article.objects.filter(category=category_model)
        # serializing the queryset
        serializer = ArticleSerializer(article, many=True)

        return Response(serializer.data)

