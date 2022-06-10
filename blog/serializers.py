from rest_framework import serializers
from .models import Article, Category

from django.contrib.auth import get_user_model

User = get_user_model()


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'id', 'is_staff')


class ArticleSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()
    category = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = ['id', 'slug', 'author', 'category', 'title', 'description', 'cover', 'created', 'updated']
    
    def get_category(self, obj):
        return {
            'name': obj.category.name
        }


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
