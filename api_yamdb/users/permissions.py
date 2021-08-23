from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    """
    Check that user is administrator.
    """
    def has_permission(self, request, view):
        """
        Override has_permission method.
        Return True if authorized user is superuser or has 'ADMIN' role.
        """
        return request.user.is_authenticated and request.user.is_admin
