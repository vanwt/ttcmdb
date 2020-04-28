from rest_framework.serializers import ModelSerializer
from ..models import Assets



class AssetSerializers(ModelSerializer):
    class Meta:
        model = Assets
        fields = [
            "id", "ip", "status", "is_active", "is_pass", "own", "idc", "project", "tags", "create_time", "change_time"
        ]
