from crypt import crypt
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from ..models import SystemUser, Assets, PushSystemUserLog
from .. import serializers

from common.ansible_api import ANSRunnser, HostGenerate


# from task.utils.dynamic_host import GenResource
# from crypt import crypt


class SystemUserViewset(ModelViewSet):
    queryset = SystemUser.objects.all()
    serializer_class = serializers.SystemuserSerializers


class PushUserView(APIView):
    def post(self, request, *args, **kwargs):
        result = {"code": 200, "msg": None}
        system_user_id = request.data.get("system_user", [])
        assets = request.data.getlist("asset", [])

        su = get_object_or_404(SystemUser, id=system_user_id)
        # 先查询同一个用户之前有没有推送，如果推送了和这次如果一样就不推送了

        # 推送的用户名
        push_user = su.username
        # 推送密码
        push_pwd = su.password
        push_group = su.group
        # 此处推送密码应该要被加密，所以用hashlib模块手动加密
        push_pwd = crypt(str(push_pwd))
        if push_group:
            args = "name={name} password={psw} group={group}".format(name=push_user, psw=push_pwd, group=push_group)
        else:
            args = "name={name} password={psw}".format(name=push_user, psw=push_pwd)
        # 用ansible 推送
        module_name = "user"

        # 生成动态主机列表
        resource = HostGenerate(assets)  # 生成动他自主机列表
        hosts = [h["host"] for h in resource]
        hosts_str = ",".join(hosts)
        # 执行命令
        ans = ANSRunnser(resource)
        ans.set_context(become_user="root", become_method="su")
        ret = ans.run_module(host_list=hosts_str, module_name=module_name, module_args=args, json=True)
        # 获取结果
        result["msg"] = ans.callback.msg
        if ret != 2:
            # 存入记录
            for host in hosts:
                pu = PushSystemUserLog()
                # 推送用户
                pu.username = su.username
                pu.pusher = request.user
                pu.host = host
                # 推送主机
                pu.save()
            # 添加到主机的系统用户
            for id in assets:
                a = Assets.objects.filter(id=id).first()
                a.system_users.add(su)
        else:
            result["code"] = 400

        return Response(result)
