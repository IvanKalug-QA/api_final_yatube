from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework.viewsets import (ModelViewSet, ReadOnlyModelViewSet,
                                     GenericViewSet)
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.exceptions import PermissionDenied, ParseError
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter

from posts.models import Post, Group, Comment, Follow
from .serializers import (PostSerializer,
                          GropuSerializer,
                          CommentSerializer,
                          FollowSerialezer)

User = get_user_model()


class ListCreateMixin(GenericViewSet, ListModelMixin, CreateModelMixin):
    pass


class PerformUpdateDestoyMixin:

    def get_post(self):
        return get_object_or_404(Post, id=self.kwargs.get('post_id'))

    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise PermissionDenied("Доступ запрещен!")
        super().perform_update(serializer)

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionDenied("Доступ запрещен!")
        super().perform_destroy(instance)


class PostViewSet(PerformUpdateDestoyMixin, ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GroupViewSet(ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GropuSerializer


class CommentViewSet(PerformUpdateDestoyMixin, ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        serializer.save(post=self.get_post(), author=self.request.user)

    def get_queryset(self):
        return self.get_post().comments.all()


class FollowViewSet(ListCreateMixin):
    queryset = Follow.objects.all()
    serializer_class = FollowSerialezer
    permission_classes = (IsAuthenticated,)
    filter_backends = (SearchFilter,)
    search_fields = ('following__username',)

    def perform_create(self, serializer):
        if self.request.user == serializer.validated_data.get('following'):
            raise ParseError('На себя подписываться нельзя!')
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return self.request.user.follows.all()
