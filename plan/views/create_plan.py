from django.shortcuts import HttpResponseRedirect, reverse, render
from django.views.generic import CreateView
from ..forms import CreateTimedTaskForm, CreateManyTaskForm
from ..tasks import *


class CreateTimedTaskView(CreateView):
    form_class = CreateTimedTaskForm
    template_name = 'plan/task-create.html'
    context_object_name = 'form'

    def form_valid(self, form):
        task = form.save(commit=False)
        # 保存name 和状态 name唯一
        status = task.status
        name = task.name
        task.create_user = self.request.user
        task.save()
        form.save_m2m()

        # 等数据库 延时
        if status == 1:
            args = """name={name} minute='{minute}' hour='{hour}' day='{day}'
                            weekday='{weekday}' month='{month}' user='{user}' job='{job}'""" \
                .format(name=task.name,
                        minute=task.minute,
                        hour=task.hour,
                        day=task.day,
                        weekday=task.week,
                        month=task.month,
                        user=task.account,
                        job=task.code
                        )
            # 执行命令， 此时的状态是激活
            ip = task.host.ip
            username = task.host.sshuser
            password = task.host.sshpwd
            port = task.host.sshport
            resource = [{"ip": ip, "username": username, "password": password, "port": port}]

            # 执行异步任务
            module_name = "cron"
            cron_async(resource, ip, module_name, args, name)
        else:
            # 步执行的话直接存
            Log_Cron.objects.create(
                cron_id=task.id,
                cron_user=task.create_user,
                cron_name=task.name,
                cron_content="添加计划任务(未执行)",
                cron_server=task.host.ip,
            )
        return HttpResponseRedirect(reverse('plan-list'))

    def form_invalid(self, form):
        return render(self.request, self.template_name, {"form": form})


class CreateManyTimedTaskView(CreateView):
    template_name = 'plan/create_many_task.html'
    success_url = 'plan/list/'
    context_object_name = 'form'
    form_class = CreateManyTaskForm

    def form_valid(self, form):
        task = form.save(commit=False)
        host = task.host
        user = self.request.user
        account = task.account
        status = task.status
        m_tasks = task.code
        del task
        # 循环存入数据库
        # 已换行来分割
        for codes in m_tasks.split('\n'):
            tag = codes.split('|')
            if len(tag) == 3:
                # 计划名
                name = tag[0]
                # 计划的代码
                code = tag[1]
                # 注释
                remark = tag[2]
                # 从代码中拆分出周期
                cycle = code.split(' ')[:5]
                # 得到后续的代码
                code = ' '.join(code.split(' ')[5:])

            elif len(tag) == 2:
                name = tag[0]
                code = tag[1]
                remark = None
                cycle = code.split(' ')[:5]
                code = ' '.join(code.split(' ')[5:])
            else:
                break
            # 存数据库
            task = TimedTask(status=status, host=host, account=account, create_user=user)
            task.name = name
            task.code = code
            task.minute = cycle[0]
            task.hour = cycle[1]
            task.day = cycle[2]
            task.month = cycle[3]
            task.week = cycle[4]
            task.remark = remark
            try:
                task.save()
            except Exception as e:
                print("创建多个任务时出错", e)
                return render(self.request, self.template_name, {"form": form})

        return HttpResponseRedirect(reverse('plan-list'))

    def form_invalid(self, form):
        return render(self.request, self.template_name, {"form": form})
