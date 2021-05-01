from rest_framework.permissions import IsAdminUser, SAFE_METHODS, BasePermission


class IsAdminUserOrReadOnly(IsAdminUser):

    def has_permission(self, request, view):

        return request.method in SAFE_METHODS or request.user.is_superuser



class TeacherOnly(BasePermission):


    def has_object_permission(self, request, view, obj):

        if request.user.is_superuser:
            return True

        return obj.teacher.user == request.user