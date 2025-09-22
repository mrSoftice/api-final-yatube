from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from rest_framework.validators import UniqueTogetherValidator

from posts.models import Comment, Follow, Group, Post

User = get_user_model()


class GroupSerializer(ModelSerializer):

    class Meta:
        model = Group
        fields = '__all__'


class PostSerializer(ModelSerializer):
    author = serializers.StringRelatedField(
        source='author.username', read_only=True)

    class Meta:
        model = Post
        fields = '__all__'


class CommentSerializer(ModelSerializer):
    author = serializers.StringRelatedField(
        source='author.username', read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('post',)


# class FollowReadSerializer(serializers.ModelSerializer):
#     user = serializers.CharField(source="user.username", read_only=True)
#     following = serializers.CharField(
#         source="following.username", read_only=True)

#     class Meta:
#         model = Follow
#         fields = ("user", "following")


class FollowReadSerializer(serializers.ModelSerializer):
    """Сериализатор для чтения — возвращает username."""
    user = serializers.CharField(source="user.username", read_only=True)
    following = serializers.CharField(
        source="following.username", read_only=True)

    class Meta:
        model = Follow
        fields = ("user", "following")


class FollowWriteSerializer(serializers.ModelSerializer):
    """
    Сериализатор для записи — принимает username,
    user подставляется автоматически.
    """
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    following = serializers.CharField()

    class Meta:
        model = Follow
        fields = ("user", "following")
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=("user", "following"),
                message="Вы уже подписаны на этого пользователя"
            )
        ]

    def validate_following(self, username):
        user = self.context["request"].user
        if user.username == username:
            raise serializers.ValidationError(
                "Нельзя подписаться на самого себя.")
        if not User.objects.filter(username=username).exists():
            raise serializers.ValidationError("Пользователь не найден.")

        return User.objects.get(username=username)

    def create(self, validated_data):
        '''Создание Follow после успешной валидации'''
        return Follow.objects.create(
            user=validated_data["user"],
            following=User.objects.get(username=validated_data['following'])
        )
