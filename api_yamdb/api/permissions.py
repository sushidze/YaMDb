from rest_framework.permissions import SAFE_METHODS, BasePermission

USER = 'user'
MODERATOR = 'moderator'
ADMIN = 'admin'


class AdminOnly(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False
        return request.user.role == ADMIN or request.user.is_superuser


class ForMeOnly(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False
        else:
            return True


class GetAllPostDeleteAdmin(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        elif request.user.is_anonymous:
            return False
        return request.user.role == ADMIN or request.user.is_superuser


class ReviewsCommentsPermission(BasePermission):
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
