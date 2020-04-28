from rest_framework import serializers
from ..models import IDC


class IdcSerializers(serializers.ModelSerializer):
    class Meta:
        model = IDC
        fields = ["name", "linkphone", "address", "network_segment", "bandwidth", "operator", "create_time"]
