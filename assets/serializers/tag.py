from rest_framework.serializers import ModelSerializer
from ..models import Tags


class TagsSerializers(ModelSerializer):
    class Meta:
        model = Tags
        fields = ["name", "create_time"]
