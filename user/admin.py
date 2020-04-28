from django.contrib import admin
from .models import User, UrlPermission, Menu, Role
from django.contrib.auth.hashers import make_password
from ttcmdb.custom_site import tt_admin_site


# Register your models here.
@admin.register(User, site=tt_admin_site)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'realname', 'phone', 'is_active']

    def __str__(self):
        return self.username

    def save_model(self, request, obj, form, change):
        pwd = obj.password
        obj.password = make_password(pwd, None, 'pbkdf2_sha256')
        return super(UserAdmin, self).save_model(request, obj, form, change)


@admin.register(Role, site=tt_admin_site)
class RoleAdmin(admin.ModelAdmin):
    list_display = ["title"]
    filter_horizontal = ("permission", "menu")


@admin.register(UrlPermission, site=tt_admin_site)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ["title", "url", "status", "method", "is_absolute"]


@admin.register(Menu, site=tt_admin_site)
class MenuAdmin(admin.ModelAdmin):
    list_display = ["title", "name", "url", "status"]
