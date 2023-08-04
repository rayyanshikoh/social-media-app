from django.urls import path, include
from rest_framework_nested import routers

from .views import *

router = routers.DefaultRouter()
router.register('posts', PostViewSet, basename='posts')

urlpatterns = [
    path('', include(router.urls)),
]
