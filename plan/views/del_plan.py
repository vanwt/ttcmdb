from django.shortcuts import HttpResponseRedirect, reverse
from django.views.generic import View
from ..tasks import *
from ..models import TimedTask


class DelTimedTask(View):
    def get(self, request, **kwargs):
        id = self.kwargs.get('id')
        try:
            task = TimedTask.get_by_id(id)
            if task.status == 1:

                ip = task.host.ip
                username = task.host.sshuser
                password = task.host.sshpwd
                port = task.host.sshport
                resource = [{"ip": ip, "username": username, "password": password, "port": port}]
                task.status = 0
                task.execution_status = 1
                task.save()
                async_delete_task.delay(resource, [ip], task.id, is_del=True)
            else:
                task.delete()
        except Exception as e:
            print("删除计划时出错", e)

        return HttpResponseRedirect(reverse('plan-list'))
