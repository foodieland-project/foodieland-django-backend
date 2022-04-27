import pytest
from ..models import Category, Recipe
from django.contrib.auth import get_user_model


User = get_user_model()


@pytest.mark.django_db
def test_recipe_create():
    """
        Test for creating a recipe by user and category
    """
    user = User.objects.create_user(email='y.amirmohamad8413@gmail.com',username='amir', password='root98765')
    category = Category.objects.create(title='fast food', slug='fast-food')
    assert user.email == 'y.amirmohamad8413@gmail.com'

    recipe = Recipe.objects.create(
        user=user,
        title='pizza',
        slug='pizza',
        category=category,
        description='some detail',
        recipe='recipe',
        info='info',
        video='./__init__.py', # wrong. it should be a video
        is_active=True,
    )

    assert recipe.title == 'pizza'
    assert recipe.slug == 'pizza'
    assert recipe.category == category
    assert recipe.user == user