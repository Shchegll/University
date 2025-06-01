from rest_framework import permissions


class CreatorOrSafeMethods(permissions.BasePermission):
    def check_request_safety(self, method):
        return method in permissions.SAFE_METHODS

    def validate_user_access(self, user, creator):
        return user == creator

    def permission(self, request, view):
        if self.check_request_safety(request.method):
            return True
        return request.user.is_authenticated

    def object_permission(self, request, view, target):
        if self.check_request_safety(request.method):
            return True
        return self.validate_user_access(request.user, target.author)
