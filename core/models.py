from django.db import models
from django.contrib.auth import get_user_model
from recipe.models import Recipe
from utilities.slug_title import slugify_instance_title


User = get_user_model()


class Category(models.Model):
    """
        Used for Recipes
        NOTE: Mabye i add it to blog model later.
    """
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=False, allow_unicode=True)
    

    class Meta:
        ordering = ('title',)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.slug is None:
            slugify_instance_title(self, save=False)
        super(Category, self).save(*args, **kwargs)



class Comment(models.Model):
    """
        The main comment model in recipe and blog pages
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment_user')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='comment_recipe', blank=True)
    # article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='c_article', null=True, blank=True)
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


class Reply(models.Model):
    """
        Used for making replies on comments in recipes and blogs
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_replies")
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name="none_replies")
    body = models.TextField(max_length=400, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    is_active = models.BooleanField(default=False)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.body

