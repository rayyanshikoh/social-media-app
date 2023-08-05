from turtle import pos
from requests import Response
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, Serializer, BaseSerializer
from rest_framework import status

from .models import Comment, Follow, Like, Post


class PostSerializer(ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'content', 'date_posted', 'author']

    def create(self, validated_data):
        user = self.context['user']
        post = Post.objects.create(author=user, **validated_data)
        return post


class EditPostSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = ['content']

    def update(self, instance, validated_data):
        if self.context['user'] == instance.author:
            instance.content = validated_data.get('content', instance.content)
            instance.save()
            return instance
        raise serializers.ValidationError('You cannot edit this post.')


class CommentSerializer(ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    post_id = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'content', 'author', 'date_posted', 'post_id']

    def create(self, validated_data):
        user = self.context['user']
        post = self.context['post']
        return Comment.objects.create(author=user, post_id=post, **validated_data)
