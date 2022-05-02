from rest_framework import serializers
from .models import Recipe


class RecipeSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    recipe_likes_count = serializers.ReadOnlyField(source="likes_count")

    class Meta:
        model = Recipe
        fields = ('title', 'user', 'recipe_likes_count')

    def get_user(self, obj):
        return obj.user.first_name if obj.user.first_name else obj.user.username
