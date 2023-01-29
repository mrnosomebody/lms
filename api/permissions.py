from rest_framework.permissions import (
    BasePermission,
    IsAdminUser,
    SAFE_METHODS
)
from api.models import StudyGroup, Student, Curator


class CanChangeStudentPermission(BasePermission):
    """
    Curator can add student to only those groups
    that are related to the specialty he manages
    """

    def has_object_permission(self, request, view, obj: Student):
        study_group_id = request.data.get('study_group')
        user: Curator = request.user

        if study_group_id:
            study_group = StudyGroup.objects.get(id=study_group_id)
            if study_group.specialty.curator.id == user.id:
                return request.user.has_perm('api.change_student')
        else:
            if obj.study_group.specialty.curator.id == user.id:
                return request.user.has_perm('api.change_student')


class CanChangeStudyGroupOrReadOnlyPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method not in SAFE_METHODS:
            return request.user and \
                request.user.is_authenticated and \
                request.user.has_perm('api.change_studygroup')
        return True


class IsOwnerOrAdminOrReadOnlyPermission(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if request.method == 'POST':
            return user and user.is_authenticated and user.is_admin
        return True

    def has_object_permission(self, request, view, obj):
        user = request.user
        if request.method in SAFE_METHODS:
            return True
        return user and user.is_authenticated \
            and (obj.id == user.id or user.is_admin)


class IsAdminUserOrReadOnlyPermission(IsAdminUser):
    def has_permission(self, request, view):
        is_admin = super().has_permission(request, view)
        return request.method in SAFE_METHODS or is_admin
