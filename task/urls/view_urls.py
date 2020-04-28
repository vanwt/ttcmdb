from django.urls import path
from ..views import *

urlpatterns = [
    path('run-module/', RunAnsModule.as_view(), name='run-ans-module'),
    path('run-module-log', AnsModuleLogView.as_view(), name='ans-module-log'),
    path('module-log/info/<int:id>/', AnsModuleLogInfoView.as_view(), name='task-module-info'),
    # playbook
    path('create-playbook/', CreatePlaybookView.as_view(), name="create-playbook"),
    path('playbooks/', PlayBooksView.as_view(), name="playbooks"),
    path('playbook-info/<int:pk>/', PlayBookInfoView.as_view(), name="playbook-info"),
    path('run-playbook/', RunPlaybookView.as_view(), name="run-playbook"),
    path('playbook-log/<int:id>/', PlayBookDetailView.as_view(), name="playbook-log"),
    path('playbook-logs/',PlayBookLogListView.as_view(),name="playbook-logs"),

    # role部分
    path('role-list/', RoleListView.as_view(), name="roles"),
    path('role/', RoleAddView.as_view(), name="role"),
    path('node-view/', NodesView.as_view(), name="node-view"),
    path('upload/', upload_file, name="task-upload"),
    path('edit-role/<int:id>/', RoleEditView.as_view(), name="change-role"),
    # 运行 role脚本
    path('run-role/', RunRoleView.as_view(), name="run-role"),
    # 获取文件路径下的文件
    path('get-detail/<int:id>/', ge_detail, name='get-detail'),
    # role脚本的所有目录
    path('get-role-script/', RoleScriptListVIew.as_view(), name="role-script"),
    # 修改role脚本
    path('detail-rolescript/', DetailRoleScript.as_view(), name='detail-role-script'),
    # 上传role 文件
    path('upload-role/',upload_role,name="upload-role"),
    # 日志
    path('role-log/<int:id>/',RoleLogView.as_view(),name="role-log"),
    path('role-logs/',RoleLogListView.as_view(),name="role-logs")

]
