from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAuthorOrIsAdmin(BasePermission):
    def has_permisson(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_authenticated)


    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return request.user and\
               (request.user == obj.user or request.user.is_staff)


class IsAuthor(BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(request.user and
                    request.user.is_authenticated and
                    request.user == obj.user)