from rest_framework import serializers
from ..models import SystemUser


class SystemuserSerializers(serializers.ModelSerializer):
    class Meta:
        model = SystemUser
        fields = ["username", "password", "group", "create_time"]
