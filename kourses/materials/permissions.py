from rest_framework import permissions


class IsModer(permissions.BasePermission):
    """Проверяет, является ли пользователь модератором."""

    def has_permission(self, request, view):
        return request.user.groups.filter(name="moder").exists()

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.method in ["PUT", "PATCH"]:
            return False


class IsOwner(permissions.BasePermission):
    """Проверяет, является ли пользователь автором"""

    def has_object_permission(self, request, view, obj):
        if obj.owner == request.user:
            return True
        return False


class IsOwnerOrModer(permissions.BasePermission):
    """Определяем является ли пользователь модератором или автором"""

    def has_object_permission(self, request, view, obj):
        if hasattr(obj, "owner") and obj.owner == request.user:
            return True
        if (
            request.user.is_authenticated
            and request.user.groups.filter(name="moder").exists()
            and request.method in ["PUT", "PATCH"]
        ):
            return True
        return False
