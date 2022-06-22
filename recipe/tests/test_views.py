from django.test import RequestFactory, TestCase, Client
from rest_framework.request import Request
from ..models import Recipe
from core.models import Category, Tag
from django.contrib.auth import get_user_model
from django.urls import reverse
from ..serializers import RecipeSerializer

# The custom user model
User = get_user_model()


class TestRecipeViews(TestCase):
    def setUp(self):
        # making client
        self.client = Client()
        self.request = RequestFactory()

        # creating user
        self.user = get_user_model().objects.create(
            email="testmail@gmail.com", password="amir4321")
        self.user.save()
        self.category = Category.objects.create(
            title='fast food', slug='fast-food')
        self.category.save()

    def test_related_recipies(self):
        recipe1 = Recipe.objects.create(
            user=self.user,
            title='pizza',
            slug='pizza',
            category=self.category,
            description='some detail',
            recipe='recipe',
            info='info',
            video='./__init__.py',  # TODO. it should be a video
            is_active=True,
        )
        recipe2 = Recipe.objects.create(
            user=self.user,
            title='pizza',
            slug='pizza2',
            category=self.category,
            description='some detail',
            recipe='recipe',
            info='info',
            video='./__init__.py',  # TODO. it should be a video
            is_active=True,
        )

        # creating some tags for recipies
        first_tag = Tag.objects.create(
            name="tag1", slug="tag1", recipe=recipe1)
        first_tag.save()

        res = self.client.get(reverse("recipe:related_recipe", kwargs={
                              'recipe_id': recipe1.id}))

        # getting the slug between response data (because slug is always unique)
        res2 = [i['slug'] for i in res.data]

        self.assertIn(recipe1.slug, res2)
        self.assertNotIn(recipe2.slug, res2)
