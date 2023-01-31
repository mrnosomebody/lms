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
        user: Curator = request.user

        if request.data.get('study_group'):
            study_group = StudyGroup.objects.get(
                id=request.data.get('study_group')
            )
        else:
            study_group = obj.study_group

        if not study_group or not study_group.specialty.curator:
            return False

        if study_group.specialty.curator.id == user.id:
            return request.user.has_perm('api.change_student')

        return False


class CanManageStudyGroupOrReadOnlyPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method not in SAFE_METHODS:
            user = request.user
            return user and \
                user.is_authenticated and \
                user.has_perm('api.add_studygroup')
        return True

    def has_object_permission(self, request, view, obj):
        if request.method not in SAFE_METHODS:
            user = request.user
            return user and \
                user.is_authenticated and \
                user.has_perm('api.change_studygroup')
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


class IsAdminOrReadOnlyPermission(IsAdminUser):
    def has_permission(self, request, view):
        is_admin = super().has_permission(request, view)
        return request.method in SAFE_METHODS or is_admin
