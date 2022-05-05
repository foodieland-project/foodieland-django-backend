from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404, render
from django.contrib.auth import get_user_model
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from utilities.pagination import PaginationHandlerMixin
from utilities.permissions import IsOwnerOrReadOnly, IsSuperUserMixin, ReadOnly
from django.http import HttpResponse
from django.shortcuts import render
from .serializers import CommentSerializer, ReplySerializer
from core.models import Comment, Reply

from rest_framework.permissions import IsAuthenticated, AllowAny
from utilities.permissions import IsOwnerOrReadOnly, IsSuperUserMixin, ReadOnly

from .models import Recipe
from .serializers import RecipeListSerializer, RecipeSerializer


class BasicPagination(PageNumberPagination):
    page_size_query_param = 'limit'


class RecipeListView(APIView):
    """
        Shows all recipies
        TODO: i should add catching with redis in this view
    """
    def get(self, request):
        # getting all results 
        recipies = Recipe.active.all()
        # serializing the queryset
        res = RecipeListSerializer(recipies, many=True)

        return Response(res.data, status=status.HTTP_200_OK)


class RecipeDetailView(APIView):
    """
        Returns all related detail to recipe
        TODO: use catching
    """
    def get(self, request, id, slug):
        # searching for the object by id, slug
        recipe = Recipe.active.get(id=id, slug=slug)
        # serializing only one object
        res = RecipeSerializer(recipe, many=False, context={'request': request})

        return Response(res.data, status=status.HTTP_200_OK)

    
class CommentListView(APIView, PaginationHandlerMixin):
    permission_classes = [ReadOnly]
    serializer_class = CommentSerializer
    pagination_class = BasicPagination

    def get(self, request, pk):
        recipe = Recipe.active.get(pk=pk)
        queryset = Comment.objects.filter(recipe=recipe)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_paginated_response(self.serializer_class(page,
                                                                           many=True, context={"request": request}).data)
        else:
            serializer = self.serializer_class(
                queryset, many=True, context={"request": request})

        return Response(serializer.data, status=status.HTTP_200_OK)


class CommentCreate(APIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = CommentSerializer

    def post(self, request, recipe_id):
        recipe = get_object_or_404(Recipe, id=self.kwargs['recipe_id'])
        body = request.POST.get('body')
        queryset = Comment.objects.create(
            user=request.user, recipe=recipe, body=body)
        if queryset:
            recipe.comments.add(queryset)
        serializer = self.serializer_class(
            queryset, partial=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CommentUpdate(APIView):
    permission_classes = [IsOwnerOrReadOnly, ]
    serializer_class = CommentSerializer

    def put(self, request, recipe_id, comment_id):
        recipe = get_object_or_404(Recipe, id=recipe_id)

        comment = get_object_or_404(Comment, pk=comment_id, recipe=recipe)
        self.check_object_permissions(request, comment)

        # self.check_object_permissions(request, question)
        serializer = self.serializer_class(
            instance=comment, data=request.data, partial=True, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentDelete(APIView):
    permission_classes = [IsOwnerOrReadOnly, ]

    def delete(self, request, recipe_id, comment_id):
        recipe = get_object_or_404(Recipe, id=recipe_id)
        comment = get_object_or_404(Comment, pk=comment_id, recipe=recipe)
        self.check_object_permissions(request, comment)

        comment.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class ReplyListView(APIView, PaginationHandlerMixin):
    """
    Shows all replies related to single comment
    """
    permission_classes = [ReadOnly]
    serializer_class = ReplySerializer
    pagination_class = BasicPagination

    def get(self, request, pk):
        queryset = Reply.objects.filter(comment__id=pk)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_paginated_response(self.serializer_class(page,
                                                                           many=True, context={"request": request}).data)  # NOTE: I removed .data
        else:
            serializer = self.serializer_class(
                queryset, many=True, context={"request": request})

        return Response(serializer.data, status=status.HTTP_200_OK)


class ReplyCreate(APIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = ReplySerializer

    def post(self, request, recipe_id, comment_id):
        recipe = get_object_or_404(Recipe, pk=recipe_id)

        comment = get_object_or_404(
            Comment, pk=comment_id, recipe__id=recipe.id)

        body = request.POST.get('body')
        queryset = Reply.objects.create(
            user=request.user, comment=comment, body=body)
        if queryset:
            comment.replies.add(queryset)
        return Response(status=status.HTTP_201_CREATED)


class ReplyUpdate(APIView):
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = ReplySerializer

    def put(self, request, recipe_id, comment_id, reply_id):
        recipe = Recipe.active.get(id=recipe_id)
        comment = Comment.objects.get(pk=comment_id, recipe=recipe)
        reply = Reply.objects.get(comment=comment, pk=reply_id)
        self.check_object_permissions(request, reply)

        # self.check_object_permissions(request, question)
        serializer = self.serializer_class(
            instance=reply, data=request.data, partial=True, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReplyDelete(APIView):
    permission_classes = [IsOwnerOrReadOnly, ]
    serializer_class = ReplySerializer

    def delete(self, request, recipe_id, comment_id, reply_id):
        recipe = Recipe.active.get(id=recipe_id)
        comment = Comment.objects.get(pk=comment_id, recipe=recipe)
        reply = Reply.objects.get(comment=comment, pk=reply_id)
        self.check_object_permissions(request, reply)

        reply.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

