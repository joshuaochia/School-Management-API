from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAdminUser,SAFE_METHODS, BasePermission
from school.models import Employees


class IsSuperUserOrReadOnly(IsAdminUser):

    def has_permission(self, request, view):
        view
        return (
            request.method in SAFE_METHODS or
            request.user.is_superuser
            )

class IsSuperUser(IsAdminUser):

    def has_permission(self, request, view):
        
        return request.user.is_superuser


class IsHROnly(BasePermission):

    def has_permission(self, request, view):
        user = request.user
        hr = get_object_or_404(Employees, user=user)
        return hr.is_hr
    
