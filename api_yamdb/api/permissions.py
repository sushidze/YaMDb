from rest_framework.permissions import SAFE_METHODS, BasePermission

USER = 'user'
MODERATOR = 'moderator'
ADMIN = 'admin'


class IsAdminUserOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == ADMIN or request.user.is_superuser


class UsersOnly(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated


class GetAllPostDeleteAdmin(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        return request.user.role == ADMIN or request.user.is_superuser


class IsAdminModeratorOwnerOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return True
        return (
                request.method in SAFE_METHODS
                or obj.author == request.user
                or request.user.role == ADMIN
                or request.user.role == MODERATOR
                or request.user.is_superuser
        )
