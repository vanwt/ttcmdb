from django.contrib import admin

# Register your models here.
from assets.models import Assets, DelAssetModel, SystemUser, Tags, IDC
from ttcmdb.custom_site import tt_admin_site


@admin.register(Assets, site=tt_admin_site)
class AssetsAdmin(admin.ModelAdmin):
    list_display = ['asset_type', 'ip', 'is_active', 'status']

    def __str__(self):
        return self.ip


@admin.register(Tags, site=tt_admin_site)
class TagsAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'create_time']

    def __str__(self):
        return self.name


@admin.register(IDC, site=tt_admin_site)
class IDCAdmin(admin.ModelAdmin):
    list_display = ["name", "linkphone", "address", "bandwidth", "operator"]

    def __str__(self):
        return self.name


@admin.register(DelAssetModel, site=tt_admin_site)
class DelAssetAdmin(admin.ModelAdmin):
    list_display = ["asset_type", "ip", "delete_time"]

    def __str__(self):
        return self.ip


@admin.register(SystemUser, site=tt_admin_site)
class ServerUserAdmin(admin.ModelAdmin):
    list_display = ["username", "password", "group"]

    def __str__(self):
        return self.username
