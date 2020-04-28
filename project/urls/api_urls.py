from rest_framework.routers import DefaultRouter
from ..api import ProjectViewSet

router = DefaultRouter()
router.register("project", ProjectViewSet)

urlpatterns = router.urls
