from django.contrib import admin
from .models import Project
from ttcmdb.custom_site import tt_admin_site


# Register your models here.

@admin.register(Project, site=tt_admin_site)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ["project_name", "create_time"]

    def __str__(self):
        return self.project_name
