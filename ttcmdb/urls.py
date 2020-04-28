# ~*~ coding: utf-8 ~*~
from __future__ import unicode_literals
from django.urls import path, include, re_path
from index import views
from ttcmdb.custom_site import tt_admin_site
from rest_framework.documentation import include_docs_urls

#
# def permission_denied(request):
#     return render(request, 'other/403.html')


# 设置403页面跳转到403
# handler403 = permission_denied
#
api_v1_urls = [
    path("assets/", include("assets.urls.api_urls")),
    path("project/", include("project.urls.api_urls")),
    path("webssh/", include("webssh.urls.api_urls")),
    path("user/", include("user.urls.api_urls"))
]
#
# api_v2_urls = [
#
# ]

app_view_urls = [
    # # db
    # path("database/", include("db.urls.view_urls")),
    # # 用户相关
    path('user/', include('user.urls.view_urls')),
    # # 资产相关
    path('assets/', include('assets.urls.view_urls')),
    # # 计划任务相关
    path('plan/', include('plan.urls.view_urls')),
    # # 执行模块,ansibleAPI
    path('task/', include('task.urls.view_urls')),
    # # 项目
    path('project/', include('project.urls.view_urls')),
    # # 远程ssh，需要有特定权限
    path('ssh/', include('webssh.urls.view_urls')),
    # # 日志
    # path('log/', include('logger.urls')),
]

urlpatterns = [
    # 主页
    path('', views.IndexView.as_view(), name='index'),
    # api
    path('api/v1/', include(api_v1_urls)),
    # path("api/v2/", include(api_v2_urls)),
    # 后台
    # path('admin/', admin.site.urls),
    path('admin/', tt_admin_site.urls, name="admin"),
    # 错误页面
    # path('403/', permission_denied),
    path('docs/', include_docs_urls(title="API Document")),

]

urlpatterns += app_view_urls
#
# urlpatterns += test_urls

# if DEBUG:
#     import debug_toolbar
#
#     urlpatterns.append(re_path(r'^__debug__/', include(debug_toolbar.urls)))
