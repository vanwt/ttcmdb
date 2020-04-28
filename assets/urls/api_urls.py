from django.urls import path
from rest_framework.routers import DefaultRouter
from ..api import *

router = DefaultRouter()
router.register("asset", AssetsViewSet)
router.register("tag", TagViewset)
router.register("idc", IdcViewset)
router.register("system-user", SystemUserViewset)

urlpatterns = [
    path('ztree/', ProjectTreeView.as_view(), name='asset-ztree'),
    # path("hardware/<str:id>/", HardwareView.as_view()),
    path("test-ping/<str:id>/", TestPingView.as_view()),
    path("push/user/", PushUserView.as_view()),
    path("hosts/", GetUserAssetsView.as_view()),
]

urlpatterns += router.urls
