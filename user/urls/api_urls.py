from django.urls import path
from rest_framework.routers import DefaultRouter
from ..api import *

router = DefaultRouter()
router.register("menu", MenuViewSet)
router.register("url/permission", UrlPermissionViewSet)
router.register("role", RoleViewSet)

urlpatterns = [
    path("menu/status/<str:id>/", ChangMenuStatusApiView.as_view()),
    path("reset/password/<str:id>/", RestPasswordApiView.as_view()),
    path("url/permission/status/<str:id>/", ChangeUrlPermissionStatus.as_view()),
    path("role/status/<str:id>/", ChangeRoleStatus.as_view()),
    path("role-users/", GetRoleAllUser.as_view()),
    path("role-permissions/", GetRoleAllPermission.as_view()),
    path("role-menus/", GetRoleAllMenu.as_view())
]

urlpatterns += router.urls
