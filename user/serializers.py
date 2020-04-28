from rest_framework import serializers
from .models import Menu, Role, UrlPermission


class MenuSerializers(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = ["id", "name", "title", "status"]


class RoleSerializers(serializers.ModelSerializer):
    users = serializers.SerializerMethodField()
    permission = serializers.SerializerMethodField()
    menu = serializers.SerializerMethodField()

    def get_users(self, row):
        return [r.realname for r in row.users.all()]

    def get_permission(self, row):
        return [p.title for p in row.permission.all()]

    def get_menu(self, row):
        return [m.title for m in row.menu.all()]

    class Meta:
        model = Role
        fields = ["id", "title", "users", "permission", "menu", "status"]


class UrlPermissionSerializers(serializers.ModelSerializer):
    class Meta:
        model = UrlPermission
        fields = ["title", "url", "method", "status"]
