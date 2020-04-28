from rest_framework.viewsets import ModelViewSet
from ..models import Tags
from common.mixins import MyDeleteMixin
from .. import serializers


class TagViewset(MyDeleteMixin, ModelViewSet):
    queryset = Tags.objects.all()
    serializer_class = serializers.TagsSerializers
