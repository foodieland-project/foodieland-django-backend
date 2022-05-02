import pytest
from django.contrib.auth import get_user_model

from recipe.models import Recipe
from ..models import Category, Comment, Reply


User = get_user_model()


@pytest.mark.django_db
def test_category_create():
    category = Category.objects.create(title='fast food', slug='fast-food')

    assert category.title == 'fast food'
    assert category.slug == 'fast-food'

@pytest.mark.django_db
def test_comment_create():
    """"
        Testing the comment create for recipies
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
    comment = Comment.objects.create(
        user=user,
        recipe=recipe,
        body="That was great",
        is_active=True
        )

    assert comment.body == "That was great"