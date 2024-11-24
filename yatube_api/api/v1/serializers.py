from rest_framework import serializers

from posts.models import Comment, Follow, Group, Post, User


class PostSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field="username",
        read_only=True
    )
    class Meta:
        model = Post
        fields = ["id", "text", "pub_date", "author", "image", "group"]
        read_only_fields = ["pub_date", "author"]


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field="username"
    )

    class Meta:
        model = Comment
        fields = ["id", "author", "post", "text", "created"]
        read_only_fields = ["id", "author", "created", "post"]


class FollowSerializer(serializers.ModelSerializer):
    following = serializers.SlugRelatedField(
        slug_field="username", queryset=User.objects.all()
    )
    user = serializers.SlugRelatedField(
        slug_field="username", 
        read_only=True,
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Follow
        fields = ["user", "following"]
        read_only_fields = ["user"]

    def validate_following(self, value):
        if self.context["request"].user == value:
            raise serializers.ValidationError(
                "Вы не можете подписаться на самого себя."
            )
        return value

    def validate(self, attrs):
        user = self.context["request"].user
        following_user = attrs.get("following")

        if Follow.objects.filter(user=user, following=following_user).exists():
            raise serializers.ValidationError(
                "Вы уже подписаны на этого пользователя."
            )
        return super().validate(attrs)

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ["id", "title", "slug", "description"]
