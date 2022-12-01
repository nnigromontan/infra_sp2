"""Настройки доступов приложения api."""

from rest_framework.permissions import SAFE_METHODS, BasePermission

from users.models import ADMIN, MODER


class AdminOnly(BasePermission):
    """Класс, описывающий настройки уровня доступа Admin."""

    def has_permission(self, request, _):
        """Доступ для чтения."""
        return request.user.role == ADMIN or request.user.is_superuser

    def has_object_permission(self, request, _, obj):
        """Доступ для записи и удаления."""
        return request.user.role == ADMIN or request.user.is_superuser


class IsAdminOrIsSelf(BasePermission):
    """Класс, описывающий настройки уровня доступа Admin или автор."""

    def has_object_permission(self, request, _, obj):
        """Доступ для записи и удаления."""
        user = obj.objects.get(username=self.request.data['username'])
        return request.user.role == ADMIN or request.user == user


class IsAdminOrReadOnly(BasePermission):
    """Класс, описывающий настройки уровня доступа Admin или read only."""

    def has_permission(self, request, _):
        """Доступ для чтения."""
        try:
            return (request.method in SAFE_METHODS
                    or request.user.role == ADMIN)
        except AttributeError:
            return False


class IsAuthorPatch(BasePermission):
    """Класс, описывающий настройки уровня доступа Автор."""

    def has_object_permission(self, request, _, obj):
        """Доступ для записи."""
        return (request.method not in ['PATCH']
                or request.user == obj.author)


class IsModeratorAuthorDelete(BasePermission):
    """Класс, описывающий настройки уровня доступа Админ или Автор."""

    def has_permission(self, request, _):
        """Доступ для удаления."""
        try:
            return (request.method not in ['DELETE']
                    or request.user.role == MODER)
        except AttributeError:
            return False
