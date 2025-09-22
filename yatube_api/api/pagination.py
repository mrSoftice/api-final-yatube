from rest_framework.pagination import LimitOffsetPagination


class CustomPostPagination(LimitOffsetPagination):
    def paginate_queryset(self, queryset, request, view=None):
        if (
            request.query_params.get('limit')
            and request.query_params.get('offset')
        ):
            return super().paginate_queryset(queryset, request, view)
        return None
