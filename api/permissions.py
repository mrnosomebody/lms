from rest_framework.permissions import BasePermission, IsAdminUser, SAFE_METHODS


class CanChangeStudentPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user and request.user.has_perm('api.change_student')


class CanChangeStudyGroupOrReadOnlyPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method not in SAFE_METHODS:
            return request.user and request.user.has_perm('api.change_studygroup')
        return True


class IsOwnerOrAdminPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.id == request.user.id or request.user.is_admin


class IsAdminUserOrReadOnlyPermission(IsAdminUser):
    def has_permission(self, request, view):
        is_admin = super().has_permission(request, view)
        return request.method in SAFE_METHODS or is_admin
