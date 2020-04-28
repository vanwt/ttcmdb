from rest_framework import serializers
from .models import Project


class ProjectSerializer(serializers.ModelSerializer):
    creator = serializers.CharField(source="creator.realname")
    auth_users = serializers.SerializerMethodField()

    def get_auth_users(self, row):
        return [u.realname for u in row.auth_users.all()]

    class Meta:
        model = Project
        fields = ["id", "project_name", "project_desc", "create_time", "auth_users", "creator"]
