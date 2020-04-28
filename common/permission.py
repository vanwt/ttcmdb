from rest_framework.permissions import BasePermission


class IsSuperUserPermission(BasePermission):
    """ 判断用户是否是超级用户 """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)
