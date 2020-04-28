from django.shortcuts import HttpResponseRedirect, reverse, render
from django.views.generic import UpdateView
from ..forms import UpdateTimedTaskForm
from ..tasks import *


class UpdateTimedTaskView(UpdateView):
    template_name = 'plan/task-update.html'
    form_class = UpdateTimedTaskForm
    context_object_name = 'form'
    success_url = '/plan/list/'
    model = TimedTask
    pk_url_kwarg = 'id'

    def form_valid(self, form):
        task = form.save(commit=False)
        task.create_user = self.request.user

        # ?? 未知原因前端写了disabled后name字段的值无法获取到，所以本办法再没保存前取上一次的名字
        last_status = TimedTask.get_by_id_only_status(task.id)

        # 因为还没提交到数据库,即得到原来的状态，
        # 如果是未激活，本次修改也是未激活，那么直接存库
        # 如果是已激活，本次修改为未激活，那么先关闭再存库
        # 如果是未激活,本次改为激活，那么直接执行并存库

        if int(task.status) == 0 and last_status == 0:
            # 本次修改，和原来的值都不是激活，直接存库
            task.save()
            form.save_m2m()

        elif last_status == 1 and int(task.status) == 0:
            # 本次修改不激活，原来是激活的，先关闭再存库
            task.save()
            form.save_m2m()

            ip = task.host.ip
            username = task.host.sshuser
            password = task.host.sshpwd
            port = task.host.sshport
            resource = [{"ip": ip, "username": username, "password": password, "port": port}]
            # 存储到表

            # 异步执行删除
            async_delete_task(resource, [ip], task.id)

        elif last_status == 0 and int(task.status) == 1:
            # 原来是未激活，本次修改为激活，先存库 再执行命令，
            task.save()
            form.save_m2m()

            ip = task.host.ip
            username = task.host.sshuser
            password = task.host.sshpwd
            port = task.host.sshport
            resource = [{"ip": ip, "username": username, "password": password, "port": port}]
            async_create_task(resource, [ip], task.id)

        else:
            # 原来是激活，现在也是激活
            # ansible 如果名字相同自动覆盖之前的？
            task.save()
            form.save_m2m()

            ip = task.host.ip
            username = task.host.sshuser
            password = task.host.sshpwd
            port = task.host.sshport
            resource = [{"ip": ip, "username": username, "password": password, "port": port}]
            async_create_task(resource, [ip], task.id)

        return HttpResponseRedirect(reverse('plan-list'))

    def form_invalid(self, form):
        return render(self.request, 'plan/task-update.html', {"form": form})
