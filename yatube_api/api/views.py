from posts.models import Comment, Follow, Group, Post
from rest_framework import filters, permissions, status, viewsets
from rest_framework.exceptions import (MethodNotAllowed, NotFound,
                                       PermissionDenied)
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from .permissions import CustomPermissionDenied, IsAuthorOrReadOnly
from .serializers import (CommentSerializer, FollowSerializer, GroupSerializer,
                          PostSerializer)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthorOrReadOnly]
    authentication_classes = [JWTAuthentication]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        try:
            return super().retrieve(request, *args, **kwargs)
        except Post.DoesNotExist:
            raise NotFound("Публикация не найдена.")

    def update(self, request, *args, **kwargs):
        partial = (
            request.method == "PATCH"
        )  # Если используется PATCH, разрешаем частичное обновление
        instance = self.get_object()  # Получаем объект по ID

        if instance.author != request.user:
            raise PermissionDenied("У вас нет прав на редактирование этой публикации.")

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)  # Проверяем валидность данных
        self.perform_update(serializer)  # Сохраняем изменения

        return Response(serializer.data)  # Возвращаем обновленные данные

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()  # Получаем объект по ID

        if instance.author != request.user:
            raise PermissionDenied("У вас нет прав на редактирование этой публикации.")

        serializer = self.get_serializer(
            instance, data=request.data, partial=True
        )  # Указываем partial=True для частичного обновления
        serializer.is_valid(raise_exception=True)  # Проверяем валидность данных
        self.perform_update(serializer)  # Сохраняем изменения

        return Response(serializer.data)  # Возвращаем обновленные данные

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()  # Получаем объект по ID

        if instance.author != request.user:
            # Возвращаем статус 403 Forbidden
            raise CustomPermissionDenied()

        self.perform_destroy(instance)  # Удаляем публикацию
        return Response(status=status.HTTP_204_NO_CONTENT)  # Возвращаем статус 204


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrReadOnly]

    def get_queryset(self):
        post_id = self.kwargs.get("post_pk")
        return Comment.objects.filter(post_id=post_id).order_by("-created")

    def list(self, request, post_pk=None):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)  # Возвращаем список комментариев

    def retrieve(self, request, post_pk, id=None):
        try:
            comment = self.get_queryset().get(id=id)
            serializer = self.get_serializer(comment)
            return Response(serializer.data)  # Возвращаем данные комментария
        except Comment.DoesNotExist:
            raise NotFound("Комментарий не найден.")

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
            return Response(serializer.data)  # Возвращаем обновленные данные
        except Comment.DoesNotExist:
            raise NotFound("Комментарий не найден.")

    def partial_update(self, request, post_pk, id=None):
        try:
            comment = self.get_queryset().get(id=id)
            if comment.author != request.user:
                raise PermissionDenied(
                    "У вас нет прав на редактирование этого комментария."
                )

            serializer = self.get_serializer(comment, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)  # Возвращаем обновленные данные
        except Comment.DoesNotExist:
            raise NotFound("Комментарий не найден.")

    def destroy(self, request, post_pk, id=None):
        try:
            comment = self.get_queryset().get(id=id)
            if comment.author != request.user:
                raise PermissionDenied("У вас нет прав на удаление этого комментария.")

            comment.delete()
            return Response(
                status=status.HTTP_204_NO_CONTENT
            )  # Возвращаем статус 204 No Content
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
            return Response(serializer.data)  # Возвращаем данные группы
        except Group.DoesNotExist:
            raise NotFound("Группа не найдена.")

    def update(self, request, pk=None):
        try:
            group = self.get_queryset().get(pk=pk)
            if not request.user.is_authenticated:
                raise PermissionDenied(
                    "Вы должны быть аутентифицированы для редактирования группы."
                )

            serializer = self.get_serializer(group, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)  # Возвращаем обновленные данные
        except Group.DoesNotExist:
            raise NotFound("Группа не найдена.")

    def partial_update(self, request, pk=None):
        try:
            group = self.get_queryset().get(pk=pk)
            if not request.user.is_authenticated:
                raise PermissionDenied(
                    "Вы должны быть аутентифицированы для редактирования группы."
                )

            serializer = self.get_serializer(group, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)  # Возвращаем обновленные данные
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
            return Response(
                status=status.HTTP_204_NO_CONTENT
            )  # Возвращаем статус 204 No Content
        except Group.DoesNotExist:
            raise NotFound("Группа не найдена.")


class FollowViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.all().order_by("id")
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ["following__username"]

    def get_queryset(self):
        # Фильтрация по текущему пользователю
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Установка текущего пользователя как подписчика
        serializer.save(user=self.request.user)
