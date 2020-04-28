from django.urls import path
from ..view import *

urlpatterns = [
    # 修改资产，删除资产
    path('list/', AssetsList.as_view(), name='assets-list'),
    path('create/', CreateAssetView.as_view(), name='assets-create'),
    path('info/<str:id>/', AssetInfo.as_view(), name='assets-info'),
    path('update/<str:id>/', UpdateAssetView.as_view(), name='assets-update'),
    path('change/active/<str:id>/', asset_active_update, name='assets-change-active'),
    # 添加标签，删除标签
    path('tag-list/', TagsView.as_view(), name='assets-tags-list'),
    # 添加基础配置，机房
    path('idc/', IDCListView.as_view(), name='assets-idcs'),
    # 系统用户
    path('system-users/', SystemUserList.as_view(), name='assets-system-user'),
    path('create/system-user/', CreateSystemUserView.as_view(), name='assets-create-system-user'),
    path('update/system-user/<str:id>/', UpdateSystemUserView.as_view(), name='assets-update-system-user'),
    # 推送用户
    path('push-user/log/', PushUserLogView.as_view(), name='assets-push-user-log'),
    # 域名列表

]
