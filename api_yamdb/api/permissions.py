from rest_framework.permissions import SAFE_METHODS, BasePermission

from users.models import ADMIN, MODER


class AdminOnly(BasePermission):
    def has_permission(self, request, _):
        return request.user.role == ADMIN or request.user.is_superuser

    def has_object_permission(self, request, _, obj):
        return request.user.role == ADMIN or request.user.is_superuser


class IsAdminOrIsSelf(BasePermission):
    def has_object_permission(self, request, _, obj):
        user = obj.objects.get(username=self.request.data['username'])
        return request.user.role == ADMIN or request.user == user


class IsAdminOrReadOnly(BasePermission):

    def has_permission(self, request, _):
        try:
            return (request.method in SAFE_METHODS
                    or request.user.role == ADMIN)
        except AttributeError:
            return False


class IsAuthorPatch(BasePermission):

    def has_object_permission(self, request, _, obj):
        return (request.method not in ['PATCH']
                or request.user == obj.author)


class IsModeratorAuthorDelete(BasePermission):

    def has_permission(self, request, _):
        try:
            return (request.method not in ['DELETE']
                    or request.user.role == MODER)
        except AttributeError:
            return False
