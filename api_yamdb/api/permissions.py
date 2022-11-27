from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdminModeratorOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or request.user.is_admin
            or request.user.is_moderator
            or obj.author == request.user
        )

    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or request.user.is_authenticated
        )


class IsAdminUserOrReadOnly(BasePermission):
    """Разрешает доступ к небезопасным методам только админам.
    К остальным - всем, в т.ч. анонам."""
    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS
            or request.user
            and request.user.is_staff
        )
   