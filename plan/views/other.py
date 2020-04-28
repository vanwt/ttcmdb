from django.http import JsonResponse
from ..models import TimedTask, Log_Cron
from common.ansible_api.ansible_api_v1 import ANSRunnser
import json


# Create your views here.
def log_cron(cron_id, cron_user, cron_name, cron_content, cron_server=None):
    """
    存储操作日志的
    :param cron_id:
    :param cron_user:
    :param cron_name:
    :param cron_content:
    :param cron_server:
    :return:
    """
    Log_Cron.objects.create(
        cron_id=cron_id,
        cron_user=cron_user,
        cron_name=cron_name,
        cron_content=cron_content,
        cron_server=cron_server,
    )
    return True


def show_crons(request, id):
    task = TimedTask.get_by_id(id)
    ip = task.host.ip
    username = task.account

    password = task.host.sshpwd
    port = task.host.sshport
    resource = [{"host": ip, "username": username, "password": password, "port": port}]
    print(resource)
    module_args = "crontab -l -u %s" % username

    ans = ANSRunnser(resource)
    ans.set_context()
    ret = ans.run_module(host_list=ip, module_name="shell", module_args=module_args)
    results = ans.callback.msg

    response = {
        "id": id,
        "code": 200,
        "result": results,
    }
    print(results)
    return JsonResponse(response)
