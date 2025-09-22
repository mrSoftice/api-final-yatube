from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from posts.models import Comment, Follow, Group, Post

User = get_user_model()


class GroupSerializer(ModelSerializer):

    class Meta:
        model = Group
        fields = '__all__'


class PostSerializer(ModelSerializer):
    author = serializers.CharField(source='author.username', read_only=True)

    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ('author', 'pub_date',)


class CommentSerializer(ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username',)

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('author', 'created', 'post')


class FollowSerializer(ModelSerializer):
    user = serializers.CharField(source='user.username', read_only=True)
    following = serializers.CharField()

    class Meta:
        model = Follow
        fields = ('user', 'following',)
        read_only_fields = ('user',)

    def validate_following(self, value):
        try:
            following = User.objects.get(username=value)
        except User.DoesNotExist:
            raise serializers.ValidationError('Пользователь не найден.')

        user = self.context['request'].user

        if user.username == value:
            raise serializers.ValidationError(
                'Нельзя подписаться на самого себя.'
            )
        if Follow.objects.filter(user=user, following=following).exists():
            raise serializers.ValidationError(
                'Вы уже подписаны на этого пользователя.'
            )
        # pdb.set_trace()
        return value

    def create(self, validated_data):
        '''Создание Follow после успешной валидации'''
        # pdb.set_trace()
        return Follow.objects.create(
            user=self.context['request'].user,
            following=User.objects.get(username=validated_data['following'])
        )
