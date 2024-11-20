from posts.models import Comment, Follow, Group, Post, User
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField


class PostSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field="username", read_only=True)

    class Meta:
        model = Post
        fields = ["id", "text", "pub_date", "author", "image", "group"]
        read_only_fields = ["pub_date", "author"]


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(read_only=True, slug_field="username")

    class Meta:
        model = Comment
        fields = ["id", "author", "post", "text", "created"]
        read_only_fields = ["id", "author", "created"]


class FollowSerializer(serializers.ModelSerializer):
    following = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all()
    )
    user = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Follow
        fields = ["user", "following"]
        read_only_fields = ["user"]

    def validate_following(self, value):
        # Проверка на попытку подписаться на самого себя
        if self.context["request"].user == value:
            raise serializers.ValidationError(
                "Вы не можете подписаться на самого себя."
            )
        return value

    def create(self, validated_data):
        # Установка текущего пользователя как подписчика
        validated_data['user'] = self.context['request'].user
        follow_instance = super().create(validated_data)
        # Возвращаем сериализованные данные для follow_instance
        return follow_instance


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ["id", "title", "slug", "description"]
