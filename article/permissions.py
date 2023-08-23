from rest_framework import permissions


class IsAdminUserOrReadOnly(permissions.BasePermission):  # 仅管理员可修改，用户只能查看
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:  # 安全方法包括GET、HEAD、OPTION；不安全方法包括POST/PUT/PATCH
            return True
        return request.user.is_superuser
