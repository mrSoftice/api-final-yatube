from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from posts.models import Comment, Follow, Group, Post

# from rest_framework.validators import UniqueTogetherValidator


User = get_user_model()


class GroupSerializer(ModelSerializer):

    class Meta:
        model = Group
        fields = '__all__'


class PostSerializer(ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Post
        fields = '__all__'


class CommentSerializer(ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('post',)


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field='username',
        default=serializers.CurrentUserDefault(),
        queryset=User.objects.all()
    )
    following = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all()
    )

    class Meta:
        model = Follow
        fields = ("user", "following")

    def validate_following(self, author):
        user = self.context['request'].user
        if user == author:
            raise serializers.ValidationError(
                {"following": "Нельзя подписаться на самого себя."}
            )
        return author

    def validate(self, data):
        user = self.context['request'].user
        if user.followers.filter(following=data['following']).exists():
            raise serializers.ValidationError(
                {"following": "Вы уже подписаны на этого пользователя."}
            )
        return data
