from django.urls import path, include
from rest_framework_nested import routers

from .views import *

router = routers.DefaultRouter()
router.register('posts', PostViewSet, basename='posts')

comments_router = routers.NestedDefaultRouter(router, 'posts', lookup='post')
comments_router.register('comments', CommentViewSet, basename='post-comments')


urlpatterns = [
    path('', include(router.urls)),
    path('', include(comments_router.urls))
]
