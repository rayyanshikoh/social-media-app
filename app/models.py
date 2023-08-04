from django.db import models
from django.conf import settings

user = settings.AUTH_USER_MODEL


class Post(models.Model):
    content = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(user, on_delete=models.CASCADE)

    def __str__(self):
        return self.content

    class Meta:
        ordering = ['-date_posted']


class Comment(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(user, on_delete=models.CASCADE)
    content = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content

    class Meta:
        ordering = ['-date_posted']


class Like(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='likes')
    author = models.ForeignKey(user, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.author.username

    class Meta:
        ordering = ['-date_posted']


class Follow(models.Model):
    from_user = models.ForeignKey(
        user, on_delete=models.CASCADE, related_name='following')
    to_user = models.ForeignKey(
        user, on_delete=models.CASCADE, related_name='followers')
    date_posted = models.DateTimeField(auto_now_add=True)
