from rest_framework import permissions
from account.services import User


class IsAdminOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return bool(
            request.method in permissions.SAFE_METHODS or
            request.user.is_superuser
        )


class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return bool(
            request.method in permissions.SAFE_METHODS or
            request.user == obj.user or
            request.user.is_superuser
        )
    
class IsAuthorOrReadOnly(permissions.BasePermission):
    message = 'Пользователь должен быть продавцом.'

    def has_permission(self, request, view):
        return bool(
            request.method in permissions.SAFE_METHODS or            
            request.user.role == User.AUTHOR or
            request.user.is_superuser
        )
    
class IsAuthor(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user.role == User.AUTHOR or
            request.user.is_superuser
        )
class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(
            request.user == obj.user or
            request.user.is_superuser
        )