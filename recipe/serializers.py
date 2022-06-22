from rest_framework import serializers
from .models import Recipe
from core.models import Comment, Reply


class RecipeListSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    # getting the counts for like field
    recipe_likes_count = serializers.ReadOnlyField(source="likes_count")

    class Meta:
        model = Recipe
        fields = ('id', 'title', 'user', 'recipe_likes_count')

    def get_user(self, obj):
        """
            Shows more usefull data for user than id
        """
        return obj.user.first_name if obj.user.first_name else obj.user.username


class RecipeSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    # getting the counts for like field
    recipe_likes_count = serializers.ReadOnlyField(source="likes_count")
    comments = serializers.HyperlinkedIdentityField(
        view_name="recipe:comment-replies")

    class Meta:
        model = Recipe
        fields = ('id', 'title', 'user', 'slug', 'category', 'description', 'recipe', 'info',
                  'video', 'likes', 'is_active', 'comments', 'active', 'recipe_likes_count')

    def get_user(self, obj):
        """
            Shows more usefull data for user than id
        """
        return obj.user.first_name if obj.user.first_name else obj.user.username


class CommentSerializer(serializers.ModelSerializer):
    replies = serializers.HyperlinkedIdentityField(
        view_name="recipe:comment-replies")
    user = serializers.SerializerMethodField("get_user")

    class Meta:
        model = Comment
        fields = ('id', 'user', 'recipe', 'body', 'created', 'replies')

    def get_user(self, obj):
        if obj.user:
            return obj.user.username,
        else:
            return None


class ReplySerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    comment = serializers.SerializerMethodField()

    class Meta:
        model = Reply
        fields = '__all__'

    def get_user(self, obj):
        if obj.user:
            return obj.user.username,
        else:
            return None

    def get_comment(self, obj):
        return obj.comment.body
