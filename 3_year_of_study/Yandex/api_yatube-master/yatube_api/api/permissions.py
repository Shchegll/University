from rest_framework import permissions


class AuthorPermission(permissions.BasePermission):
    """Grant access if user is object author OR method is safe."""

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user
