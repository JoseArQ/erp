from rest_framework import permissions
from .enums import UserRole


class IsAdmin(permissions.BasePermission):
    """Allow access only to admin users."""
    def has_permission(self, request, view):
        return bool(
            request.user 
            and request.user.is_authenticated 
            and request.user.role == UserRole.ADMIN.value
        )


class IsAdminOrEmployee(permissions.BasePermission):
    """Allow access to both admin and employee users."""
    def has_permission(self, request, view):
        return bool(
            request.user 
            and request.user.is_authenticated 
            and request.user.role in [UserRole.ADMIN.value, UserRole.EMPLOYEE.value]
        )
