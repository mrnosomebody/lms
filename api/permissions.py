from rest_framework.permissions import BasePermission


class CreateOrOwnerPermission(BasePermission):

    def has_permission(self, request, view):
        return request.method == 'POST'

    def has_object_permission(self, request, view, obj):
        return obj.id == request.user.id
