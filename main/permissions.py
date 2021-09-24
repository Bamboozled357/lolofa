from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAuthorOrIsAdmin(BasePermission):
    def has_permisson(self, request, view):
        """Срабатывает при действиях, в которых не нужен конкретный объект
        eg: list и create.
        """
        if request.method in SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_authenticated)


    def has_object_permission(self, request, view, obj):
        """Срабатывает при действиях, в которых используется один конкретный объект
         т.е retrieve, update, delete
         Всегда срабатывает после метода has_permission, т.е если там будет ошибка, то дальше
         программа не пойдет.
         """
        if request.method in SAFE_METHODS:
            return True
        return request.user and\
               (request.user == obj.user or request.user.is_staff)


class IsAuthor(BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(request.user and
                    request.user.is_authenticated and
                    request.user == obj.user)

class IsOwnerOrStaffOrReadOnly(BasePermission):

    def has_object_permission(self, request, view, obj):
        return bool(
            request.method in SAFE_METHODS or
            request.user and
            request.user.is_authenticated and obj.owner == request.user
        )

