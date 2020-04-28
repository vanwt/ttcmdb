from rest_framework.viewsets import ModelViewSet
from .models import Project
from .serializers import ProjectSerializer
from common.mixins import MyDeleteMixin


class ProjectViewSet(MyDeleteMixin, ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
