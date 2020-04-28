from common.ansible_api.ansible_api_v1 import ANSRunnser
from celery import shared_task
from .models import TimedTask, Log_Cron
# from logger.models import OperatingLog
from datetime import datetime


@shared_task
def cron_delay(resource, ip, module_name, module_args):
    ans = ANSRunnser(resource)
    ans.set_context(become_method="su", become_user="root")
    ans.run_module(host_list=[ip], module_name=module_name, module_args=module_args)


@shared_task
def cron_async(resource, ip, module_name, module_args, name, is_del=False):
    try:
        task = TimedTask.objects.get(name=name)
    except TimedTask.DoesNotExist:
        return "FAILURE"

    if type(ip) is list:
        ip = ",".join(ip)
    # 能查到再执行
    ans = ANSRunnser(resource)
    ans.set_context(become_method="su", become_user="root")
    ans.run_module(host_list=ip, module_name=module_name, module_args=module_args)
    # 已经执行完了，保存状态
    if is_del:
        task.delete()
    else:
        task.execution_status = 2
        task.save()
    # 添加日志
    Log_Cron.objects.create(
        cron_id=task.id,
        cron_user=task.create_user,
        cron_name=task.name,
        cron_content="添加计划任务(执行)",
        cron_server=task.host.ip,
    )
    return 'over'


@shared_task
def async_create_task(resource, ip, task_id):
    try:
        ans = ANSRunnser(resource)
        ans.set_context(become_method="su", become_user="root")
        task = TimedTask.get_by_id(task_id)

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
        ret = ans.run_module(host_list=ip, module_name="cron", module_args=args)
        # 取出result的值
        if ret == 0:
            task.execution_status = 2
            task.save()
        else:
            # 存日志数据库
            task.execution_status = 3
            task.save()

    except Exception as e:
        print('task err', e)
        return e

    Log_Cron.objects.create(
        cron_id=task.id,
        cron_user=task.create_user,
        cron_name=task.name,
        cron_content="添加计划任务",
        cron_server=task.host.ip,
    )
    return 'over'


@shared_task
def async_delete_task(resource, ip, task_id, is_del=None):
    task = TimedTask.get_by_id(task_id)
    print('no', task.name)
    try:
        ans = ANSRunnser(resource)
        ans.set_context(become_method="su", become_user="root")
        ret = ans.run_module(host_list=ip, module_name="cron",
                             module_args="name={name} state=absent".format(name=task.name))
    except Exception as e:
        task.execution_status = 3
        task.save()
        return e
    else:
        if ret == 0:
            if is_del:
                task.delete()
            else:
                task.execution_status = 2
                task.save()
        else:
            task.execution_status = 3
            task.save()
            return "ansible task 执行失败"
    return 'over'

#
#
# @shared_task
# def save_log(user=None, ip=None, action=None, resource=None, operating=None):
#     """
#     用于存储针对资源的操作异步执行
#     :param user: 用户关系: 一对一关系
#     :param ip:  IP地址 可以为空
#     :param action: 操作以动作  有增删改查
#     :param resource:  操作的资源 ，针对于哪个表
#     :param operating:  操作具体内容
#     :return:  True 或 False
#     """
#     try:
#         log = OperatingLog(
#             user=user,
#             ip=ip,
#             action=action,
#             resource=resource,
#             operating=operating,
#             create_time=datetime.now()
#         )
#         log.save()
#     except Exception as e:
#         print(e, '存储操作日志错误')
#         return False
#     return True
