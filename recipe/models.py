from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from utilities.slug_title import slugify_instance_title
from .managers import ActiveRecipesManager

User = get_user_model()


class Recipe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    slug = models.SlugField()
    category = models.ForeignKey('core.Category', on_delete=models.CASCADE)
    description = models.TextField()
    recipe = models.TextField()
    info = models.TextField()
    video = models.FileField()
    likes = models.ManyToManyField(User, blank=True, related_name='recipe_like')
    is_active = models.BooleanField(default=True)
    comments = models.ManyToManyField('core.Comment', blank=True, related_name='recipe_comment')
    active = ActiveRecipesManager() # filters all recipies base on is_active field

    class Meta:
        ordering = ('id',)

    def get_absolute_url(self):
        return reverse("recipe:recipe_detail", kwargs={'pk': self.pk, 'slug': self.slug})

    def likes_count(self):
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
    


