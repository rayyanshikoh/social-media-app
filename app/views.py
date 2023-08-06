from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied

from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import permissions
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework import status

from .models import Post, Comment, Like, Follow
from .serializers import EditPostSerializer, PostSerializer, CommentSerializer, ViewPostSerializer


class PostViewSet(ListModelMixin, RetrieveModelMixin, CreateModelMixin, DestroyModelMixin, UpdateModelMixin, GenericViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    http_method_names = ['get', 'post', 'patch', 'delete', 'option', 'head']

    permission_classes = [IsAdminUser]

    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return EditPostSerializer
        elif self.request.method == 'GET':
            if 'pk' in self.kwargs:
                return ViewPostSerializer
        return PostSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        elif self.request.method == 'POST':
            return [IsAuthenticated()]
        elif self.request.method in ['PATCH', 'DELETE']:
            if self.request.user == Post.objects.get(pk=self.kwargs['pk']).author or self.request.user.is_staff:
                return [IsAuthenticated()]
        return [IsAdminUser()]

    def get_serializer_context(self):
        return {'user': self.request.user}

    @action(detail=False, methods=['get', 'destroy', 'put'], url_path='my-posts')
    def my_posts(self, request):
        posts = Post.objects.filter(author=request.user)
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)


class CommentViewSet(CreateModelMixin, ListModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, GenericViewSet):
    permission_classes = [IsAdminUser]

    http_method_names = ['get', 'post', 'patch', 'delete', 'option', 'head']

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return [AllowAny()]
        elif self.request.method == 'POST':
            return [IsAuthenticated()]
        else:
            if self.request.user == Comment.objects.get(pk=self.kwargs['pk']).author or self.request.user.is_staff:
                return [IsAuthenticated()]
            else:
                return [IsAdminUser()]

    def get_serializer_context(self):
        return {'user': self.request.user, 'post': self.kwargs['post_pk']}

    def get_queryset(self):
        return Comment.objects.filter(post_id=self.kwargs['post_pk']).order_by('date_posted')

    serializer_class = CommentSerializer
