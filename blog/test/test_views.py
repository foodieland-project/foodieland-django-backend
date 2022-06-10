from django.test import TestCase, Client
from rest_framework import status
from django.contrib.auth import get_user_model
from ..models import Article, Category
from django.urls import reverse
from django.contrib.sites.models import Site


class ArticleTest(TestCase):
    def setUp(self):
        # making client
        self.client = Client()

        # creating user
        self.user = get_user_model().objects.create(email="testmail@gmail.com", password="amir4321")
        self.user.save()

        # creating category
        self.category = Category.objects.create(name="django", slug="django")
        self.category.save()

    def test_create_article(self):

        # creating the user using payload
        article = Article.objects.create(author=self.user, category=self.category, title='this is title',
                                         slug='this-is-slug', description='this is description', cover="__init__.py")

        # sending request
        res = self.client.get(reverse('blog:article_detail', args=(article.id, article.slug)))

        # checking data
        self.assertEqual(res.data['title'], article.title)  
        self.assertEqual(res.data['category']['name'], article.category.name)
        self.assertEqual(res.data['slug'], article.slug)
        self.assertEqual(res.data['description'], article.description)
        self.assertEqual(res.data['cover'], f'http://testserver/media/{article.cover}')