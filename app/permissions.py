from math import perm
from rest_framework import permissions


# class IsAuthor(BasePermission):
#     def has_object_permission(self, request, view, obj):
#         if request.method in SAFE_METHODS:
#             return True
#         # return obj.author == request.user
#         return obj.author == request.user or request.user.is_staff


class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_staff)
