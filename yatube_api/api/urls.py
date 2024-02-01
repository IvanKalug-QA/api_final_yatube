from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import (PostViewSet,
                    CommentViewSet,
                    GroupViewSet,
                    FollowViewSet)

router = SimpleRouter()
router.register('posts', PostViewSet)
router.register(r'posts/(?P<post_id>\d+)/comments', CommentViewSet,
                basename='comments')
router.register('groups', GroupViewSet)
router.register('follow', FollowViewSet, basename='following')


urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/', include('djoser.urls.jwt'))
]
