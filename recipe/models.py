from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

from utilities.slug_title import slugify_instance_title

User = get_user_model()


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment_user')
    recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE, related_name='comment_recipe', blank=True)
    # article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='c_article', null=True, verbose_name="مقاله", blank=True)
    body = models.CharField(max_length=400, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    replies = models.ManyToManyField('Reply', blank=True, related_name='comment_replies')
    is_active = models.BooleanField(default=False)

    def is_comment_active(self):
        if self.is_active:
            return True
        else:
            return False
    is_comment_active.boolean = True


    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.body


class Category(models.Model):
    title = models.CharField(max_length=100, null=True, blank=True)
    slug = models.SlugField(unique=False, allow_unicode=True, null=True, blank=True)


    class Meta:
        ordering = ('title',)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.slug is None:
            slugify_instance_title(self, save=False)
        super(Category, self).save(*args, **kwargs)

class Recipe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    slug = models.SlugField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField()
    recipe = models.TextField()
    info = models.TextField()
    video = models.FileField()
    likes = models.ManyToManyField(User, blank=True, related_name='recipe_like')
    is_active = models.BooleanField(default=True)
    comments = models.ManyToManyField(Comment, blank=True, related_name='recipe_comment')

    class Meta:
        ordering = ('id',)

    def get_absolute_url(self):
        return reverse("recipe:recipe_detail", kwargs={'pk': self.pk, 'slug': self.slug})

    def likes_count(self=None, d=None):
        return self.likes.count()

    def is_recipe_active(self):
        if self.is_active == True:
            return True
        else:
            return False
    is_recipe_active.boolean = True

    def save(self, *args, **kwargs):
        if self.slug is None:
            slugify_instance_title(self, save=False)
        super(Recipe, self).save(*args, **kwargs)
    

class Reply(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_replies")
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name="none_replies")
    body = models.TextField(max_length=400, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    is_active = models.BooleanField(default=False)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.body
