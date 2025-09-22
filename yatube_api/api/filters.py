import django_filters

from posts.models import Post


class PostFilter(django_filters.FilterSet):
    # алиасы
    author = django_filters.CharFilter(
        field_name="author__username", lookup_expr="iexact")
    group = django_filters.CharFilter(
        field_name="group__title", lookup_expr="icontains")

    class Meta:
        model = Post
        fields = ["author", "group"]
