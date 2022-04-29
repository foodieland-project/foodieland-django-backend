import pytest
from ..models import Category

@pytest.mark.django_db
def test_category_create():
    category = Category.objects.create(title='fast food', slug='fast-food')

    assert category.title == 'fast food'
    assert category.slug == 'fast-food'