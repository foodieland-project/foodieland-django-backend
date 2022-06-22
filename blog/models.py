from django.conf import settings
from django.db import models
from django.db import models
from django.core.files.images import get_image_dimensions
from ckeditor.fields import RichTextField
from django.contrib.auth import get_user_model
from .managers import ActiveManager

User = get_user_model()


def validate_cover(value):
    """
    validating the file size (the allowed size should be set in settings)
    """
    size = get_image_dimensions(value)
    if size > settings.MAX_UPLOAD_ADMIN_SIZE:
        raise ValueError("Please keep file size under 2 MB")


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)
    objects = models.Manager()
    active = ActiveManager()

    class Meta:
        verbose_name = "Article Category"
        verbose_name_plural = "Article Categories"

    def __str__(self):
        return self.name


class Article(models.Model):
    """
        NOTE: 
            - The author field must be null because of on_delete
            - The descritpion will change to ckediter fields
            - With is_active field, we will filter the articles
    """
    STATUS_CHOICES = (
        ('d', 'draft'),
        ('p', "publish"),
    )
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    slug = models.SlugField(unique=True)
    description = RichTextField()
    cover = models.ImageField(upload_to='backend/media')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    objects = models.Manager()
    active = ActiveManager()

    class Meta:
        verbose_name = "Article"
        verbose_name_plural = "Article"

    def __str__(self):
        return self.title
