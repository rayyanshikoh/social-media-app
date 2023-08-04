from ast import Is
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied

from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework import status

from .models import Post, Comment, Like, Follow
from .serializers import EditPostSerializer, PostSerializer


class PostViewSet(ListModelMixin, RetrieveModelMixin, CreateModelMixin, DestroyModelMixin, UpdateModelMixin, GenericViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    http_method_names = ['get', 'post', 'put', 'delete']

    permission_classes = [IsAdminUser]

    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return EditPostSerializer
        return PostSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated()]

    def get_serializer_context(self):
        return {'user': self.request.user}

    # The following two methods are needed to overwrite the default behavior of the destroy method, for more detail,
    # visit the DestroyModelMixin class in rest_framework.mixins

    def destroy(self, request, *args, **kwargs):
        try:
            # This is to invoke the default behavior of the destroy method; which implements perform_destroy method which we have overwritten
            return super().destroy(request, *args, **kwargs)
        except PermissionDenied as e:
            return Response(status=status.HTTP_403_FORBIDDEN)

    # Overwriting the default perform_destroy method
    def perform_destroy(self, instance):
        if instance.author != self.request.user and not self.request.user.is_staff:
            raise PermissionDenied('You cannot delete this post.')
        instance.delete()

    @action(detail=False, methods=['get', 'destroy', 'put'], url_path='my-posts')
    def my_posts(self, request):
        posts = Post.objects.filter(author=request.user)
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
