from django.contrib import admin
from .models import SessionLog, CodeLog
from ttcmdb.custom_site import tt_admin_site


@admin.register(SessionLog, site=tt_admin_site)
class SessionLogAdmin(admin.ModelAdmin):
    list_display = ['host', 'user', 'ssh_user', 'create_time', 'end_time', 'status']


@admin.register(CodeLog, site=tt_admin_site)
class CodeLogAdmin(admin.ModelAdmin):
    list_display = ['id', 'connection', 'command', 'addtime']
