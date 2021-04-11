from rest_framework import permissions
from rest_framework.permissions import IsAdminUser


class EmployeeOrReadOnly(permissions.BasePermission):
    """
    If user is admin POST method is True,
    else, Read Only
    """

    def has_permission(self, request, view):

        if request.user.is_superuser:
            return True

        return view.action in ['list', 'retrieve', 'update', 'partial_update']

    def has_object_permission(self, request, view, obj):

        if request.method in permissions.SAFE_METHODS:
            return True

        if request.user.is_superuser:
            return True

        return obj.user == request.user


class IsAdminUserOrReadOnly(IsAdminUser):

    def has_permission(self, request, view):

        return (
            request.method in permissions.SAFE_METHODS or
            request.user.is_superuser
            )
