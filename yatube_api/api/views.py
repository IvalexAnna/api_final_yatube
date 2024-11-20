from rest_framework import filters, permissions, serializers, status, viewsets
from rest_framework.exceptions import (MethodNotAllowed, NotFound,
                                       PermissionDenied)
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from posts.models import Comment, Follow, Group, Post
from .permissions import IsAuthorOrReadOnly
from .serializers import (CommentSerializer,
                          FollowSerializer,
                          GroupSerializer,
                          PostSerializer)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthorOrReadOnly]
    authentication_classes = [JWTAuthentication]
    pagination_class = LimitOffsetPagination

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data["author"] = request.user
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        partial = request.method == "PATCH"
        instance = self.get_object()

        if instance.author != request.user:
            raise PermissionDenied(
                "У вас нет прав на редактирование этой публикации."
            )

        serializer = self.get_serializer(
            instance, data=request.data,
            partial=partial
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance.author != request.user:
            raise PermissionDenied(
                "У вас нет прав на удаление этой публикации."
            )

        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrReadOnly]

    def get_queryset(self):
        post_id = self.kwargs.get("post_pk")
        return Comment.objects.filter(post_id=post_id).order_by("-created")

    def list(self, request, post_pk=None):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, post_pk, id=None):
        try:
            comment = self.get_queryset().get(id=id)
            serializer = self.get_serializer(comment)
            return Response(serializer.data)
        except Comment.DoesNotExist:
            raise NotFound("Комментарий не найден.")

    def create(self, request, post_pk=None):
        data = request.data.copy()
        data["post"] = post_pk
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save(post_id=post_pk, author=request.user)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, post_pk, id=None):
        try:
            comment = self.get_queryset().get(id=id)
            if comment.author != request.user:
                raise PermissionDenied(
                    "У вас нет прав на редактирование этого комментария."
                )

            serializer = self.get_serializer(comment, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        except Comment.DoesNotExist:
            raise NotFound("Комментарий не найден.")

    def partial_update(self, request, post_pk, id=None):
        try:
            comment = self.get_queryset().get(id=id)
            if comment.author != request.user:
                raise PermissionDenied(
                    "У вас нет прав на редактирование этого комментария."
                )

            serializer = self.get_serializer(
                comment,
                data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        except Comment.DoesNotExist:
            raise NotFound("Комментарий не найден.")

    def destroy(self, request, post_pk, id=None):
        try:
            comment = self.get_queryset().get(id=id)
            if comment.author != request.user:
                raise PermissionDenied(
                    "У вас нет прав на удаление этого комментария."
                )

            comment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Comment.DoesNotExist:
            raise NotFound("Комментарий не найден.")


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all().order_by("id")
    serializer_class = GroupSerializer
    permission_classes = [IsAuthorOrReadOnly]
    pagination_class = None

    def create(self, request, *args, **kwargs):
        raise MethodNotAllowed("Группы можно создавать только через админку.")

    def retrieve(self, request, pk=None):
        try:
            group = self.get_queryset().get(pk=pk)
            serializer = self.get_serializer(group)
            return Response(serializer.data)
        except Group.DoesNotExist:
            raise NotFound("Группа не найдена.")

    def update(self, request, pk=None):
        try:
            group = self.get_queryset().get(pk=pk)
            if not request.user.is_authenticated:
                raise PermissionDenied(
                    "Вы должны быть аутентифицированы"
                )

            serializer = self.get_serializer(group, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        except Group.DoesNotExist:
            raise NotFound("Группа не найдена.")

    def partial_update(self, request, pk=None):
        try:
            group = self.get_queryset().get(pk=pk)
            if not request.user.is_authenticated:
                raise PermissionDenied(
                    "Вы должны быть аутентифицированы."
                )

            serializer = self.get_serializer(
                group,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        except Group.DoesNotExist:
            raise NotFound("Группа не найдена.")

    def destroy(self, request, pk=None):
        try:
            group = self.get_queryset().get(pk=pk)
            if not request.user.is_authenticated:
                raise PermissionDenied(
                    "Вы должны быть аутентифицированы для удаления группы."
                )

            group.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Group.DoesNotExist:
            raise NotFound("Группа не найдена.")


class FollowViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.all().order_by("id")
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ["following__username"]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        following_user = serializer.validated_data["following"]
        if Follow.objects.filter(
            user=self.request.user, following=following_user
        ).exists():
            raise serializers.ValidationError(
                "Вы уже подписаны на этого пользователя."
            )
        serializer.save(user=self.request.user)
