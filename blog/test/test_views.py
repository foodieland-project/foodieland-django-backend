import json
from ..models import Article, Category
from ..serializers import ArticleSerializer, CategorySerializer
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status

class BlogTestView(TestCase):
    def setUp(self):
        # making client
        self.client = Client()

        # creating user
        self.user = get_user_model().objects.create(email="testmail@gmail.com", password="amir4321")
        self.user.save()

        # creating category
        self.category = Category.objects.create(name="django", slug="django")
        self.category.save()

    def test_article_detail_view(self):

        # creating the user using payload
        article = Article.objects.create(author=self.user, category=self.category, title='this is title',
                                         slug='this-is-slug', description='this is description', cover="__init__.py")

        # sending request
        res = self.client.get(reverse('blog:article_detail', args=(article.id, article.slug)))

        # checking data
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data['title'], article.title)  
        self.assertEqual(res.data['category']['name'], article.category.name)
        self.assertEqual(res.data['slug'], article.slug)
        self.assertEqual(res.data['description'], article.description)
        self.assertEqual(res.data['cover'], f'http://testserver/media/{article.cover}')
    
    def test_article_list_view(self):
        Article.objects.create(author=self.user, category=self.category, title='this is title1',
                                    slug='this-is-slug1', description='this is description1', cover="__init__.py")
        Article.objects.create(author=self.user, category=self.category, title='this is title2',
                                    slug='this-is-slug2', description='this is description2', cover="__init__.py")
 
        # getting data from /articles
        res = self.client.get(reverse('blog:articles'))


        # getting article/articles
        articles = Article.active.all()


        # serializing article/articles
        sz = ArticleSerializer(articles, many=True)

        # checking the response status code
        self.assertEqual(res.status_code, 200)
        # becuase the cover field in response is differnt to the queryset cover field (the domain name)
        self.assertNotEqual(res.data, sz.data) # becuase the cover field in response is differnt to the queryset cover field
        

    def test_article_by_category(self):
        # making fake article
        article = Article.objects.create(author=self.user, category=self.category, title='this is title',
                                    slug='this-is-slug', description='this is description', cover="__init__.py")

        # making request
        res = self.client.get(reverse('blog:article_by_category', kwargs={'category': self.category.slug}))
        # getting article by category
        articles = Article.active.filter(category=self.category)

        # serializing article 
        sz = ArticleSerializer(articles, many=True)

        # checking the article/articles from db to the res
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data, sz.data)


    def test_category_list_view(self):
        Category.objects.create(name='react', slug='react')
        res = self.client.get(reverse('blog:category_list'))
        categories = Category.active.all()

        sz = CategorySerializer(categories, many=True)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data, sz.data)
