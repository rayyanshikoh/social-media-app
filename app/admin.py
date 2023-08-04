from django.contrib import admin
from .models import Post, Comment, Like, Follow


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'content', 'author', 'date_posted']
