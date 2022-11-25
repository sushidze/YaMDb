from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminUserOrReadOnly(BasePermission):
    """Разрешает доступ к небезопасным методам только админам.
    К остальным - всем, в т.ч. анонам."""
    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS
            or request.user
            and request.user.is_staff
        )
    # по такой схеме реализован похожий пермишн в drf.
    # полагаю, лишняя проверка request.user оптимизирует вычисление
