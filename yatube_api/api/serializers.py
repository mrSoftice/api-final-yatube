from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from posts.models import Comment, Group, Post


class GroupSerializer(ModelSerializer):

    class Meta:
        model = Group
        fields = '__all__'


class PostSerializer(ModelSerializer):
    author = serializers.CharField(source='author.username')

    class Meta:
        fields = '__all__'
        model = Post
        read_only_fields = ('author', 'pub_date',)


class CommentSerializer(ModelSerializer):
    author = serializers.SlugRelatedField(
        source='author.username', slug_field='username')

    class Meta:
        fields = '__all__'
        model = Comment
        read_only_fields = ('author', 'created', 'post')
