from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Доступ к изменению/удалению есть только у автора объекта.
    Для остальных пользователей доступ только для чтения.
    """

    def has_object_permission(self, request, view, obj):
        return request.method in permissions.SAFE_METHODS or (
            obj.author == request.user)
