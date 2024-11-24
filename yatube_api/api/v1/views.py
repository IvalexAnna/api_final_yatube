from rest_framework import filters, permissions, status, viewsets, mixins
from rest_framework.exceptions import PermissionDenied
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from posts.models import Comment, Follow, Group, Post
from .permissions import IsAuthorOrReadOnly
from .serializers import (
    CommentSerializer,
    FollowSerializer,
    GroupSerializer,
    PostSerializer,
)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthorOrReadOnly]
    authentication_classes = [JWTAuthentication]
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        instance = self.get_object()
        if instance.author != self.request.user:
            raise PermissionDenied(
                "У вас нет прав на редактирование этой публикации."
            )
        serializer.save()

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionDenied(
                "У вас нет прав на удаление этой публикации."
            )
        super().perform_destroy(instance)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrReadOnly]

    def get_post_id(self):
        return self.kwargs.get("post_pk")

    def get_queryset(self):
        post_id = self.get_post_id()
        comments = Comment.objects.filter(post_id=post_id).order_by("-created")
        return comments

    def perform_create(self, serializer):
        post_id = self.get_post_id()
        serializer.save(post_id=post_id, author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all().order_by("id")
    serializer_class = GroupSerializer
    permission_classes = [IsAuthorOrReadOnly]
    pagination_class = None

    def get_group(self, pk):
        return self.get_object()


class FollowViewSet(mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    viewsets.GenericViewSet):
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    filter_backends = (filters.SearchFilter,)
    search_fields = ["following__username"]

    def get_queryset(self):
        return Follow.objects.all().filter(user=self.request.user)
