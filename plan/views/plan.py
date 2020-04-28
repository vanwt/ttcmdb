import json
from django.http import QueryDict, JsonResponse
from django.shortcuts import get_object_or_404
from django_filters.views import FilterView
from ..filters import PlanFilter
from ..models import TimedTask, Log_Cron
from ..tasks import cron_async


class TaskListView(FilterView):
    template_name = 'plan/task-list.html'
    queryset = TimedTask.get_all()
    filterset_class = PlanFilter

    def delete(self, request, **kwargs):
        ret = {'code': 200, 'error': None, }
        body = QueryDict(request.body)
        id = body.get('id')
        try:
            task = get_object_or_404(TimedTask, id=id)
            if task.status == 1:
                name = task.name
                task.execution_status = 1
                ip = task.host.ip
                username = task.host.sshuser
                password = task.host.sshpwd
                port = task.host.sshport
                task.save()
                # 执行
                # time.sleep(0.1)
                resource = [{"ip": ip, "username": username, "password": password, "port": port}]
                module_name = "cron"
                args = "name={name} state=absent".format(name=name)
                cron_async(resource, ip, module_name, args, name, is_del=True)
                Log_Cron.objects.create(
                    cron_id=task.id,
                    cron_user=task.create_user,
                    cron_name=task.name,
                    cron_content="删除计划任务",
                    cron_server=task.host.ip,
                )
            else:
                Log_Cron.objects.create(
                    cron_id=task.id,
                    cron_user=task.create_user,
                    cron_name=task.name,
                    cron_content="删除计划任务",
                    cron_server=task.host.ip,
                )
                task.delete()
        except Exception as e:
            ret["error"] = str(e)
            ret["code"] = 400
            print(e)
        return JsonResponse(ret)
