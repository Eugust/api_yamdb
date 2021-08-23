from rest_framework import permissions


class OwnerOrReadOnly(permissions.BasePermission):
    """
    Рвзрешает доступ к безопасным методам
    (чтение) всем пользователям,
    а авторизованным и администрации - ко всем прочим.
    """
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user and request.user.is_authenticated:
            return (request.user.is_admin
                    or request.user.is_moderator
                    or obj.author == request.user)
        return False
