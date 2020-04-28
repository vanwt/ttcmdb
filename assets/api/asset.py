from django.db.models import Q
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from project.models import Project
from ..models import Assets, DelAssetModel
from .. import serializers
# from logger.tasks import save_log
# from task.utils.ansible_api import ANSRunner
from paramiko import SSHClient, AutoAddPolicy
import subprocess, telnetlib


class AssetsViewSet(ModelViewSet):
    queryset = Assets.objects.all()
    serializer_class = serializers.AssetSerializers

    def destroy(self, request, *args, **kwargs):
        asset = self.get_object()
        # 存入删除记录表
        try:
            asset_del = DelAssetModel()
            asset_del.ip = asset.ip
            asset_del.cpu = asset.cpu
            asset_del.logical_cpu = asset.logical_cpu
            asset_del.asset_type = asset.asset_type
            asset_del.create_time = asset.create_time
            asset_del.sshuser = asset.sshuser
            asset_del.sshpwd = asset.sshpwd
            asset_del.save()
            # 删除
            self.perform_destroy(asset)
        except Exception as e:
            return Response({"code": 400, "msg": "删除失败！" + str(e)})
        else:
            # 写入到数据库
            ip = request.META.get('REMOTE_HOST')
            msg = '删除资产: %s' % asset.ip
            # save_log.delay(request.user.realname, action='del', resource='Assets资产表', operating=msg, ip=ip)
        return Response({"code": 200, "msg": "删除成功！"})


class ProjectTreeView(APIView):
    permission_classes = []

    def get(self, request, **kwargs):
        """
            资产树： 如果是超级用户，就显示全部树就可以，如果是普通用户，只显示含有该用户的项目和业务线
            :param request:
            :return:
            """
        rid = 1
        result = [{"name": "全部", "id": rid, "pId": 0, "url": "/assets/list/", "target": "_self", "open": "true",
                   "is_Parent": "true"}, ]
        user = request.user
        projects = Project.get_all()
        if user.is_superuser:
            # 循环获得业务县
            for child in projects:
                url = "/assets/list/?project=" + child.project_name
                result.append(
                    {"name": child.project_name, "id": rid, "pId": 1, "url": url, "open": "true", "target": "_self"})
                # 把这个业务线添加到default中
                rid += 1
        else:
            # 查询业务线的项目含该用户的业务线
            # 现在是非业务线下用户的不可见
            pid = 1  # 业务线id 1 * 10 + pid
            for p in Project.objects.filter(
                    Q(auth_users=user) | Q(creator=user)).prefetch_related("auth_users"):
                purl = "/assets/list/?project=" + p.project_name

                result.append({"name": p.project_name, "id": pid, "pId": pid * 10, "url": purl, "target": "_self"})

                pid += 1

        return Response(result)


#
# class HardwareView(APIView):
#     permission_classes = []
#
#     def get(self, request, **kwargs):
#         res = {"code": 200, "result": None, "error": None}
#         asset = get_object_or_404(Assets, id=self.kwargs.get("id", None))
#         aip = asset.ip
#         module = 'setup'
#         resource = [{"ip": aip, "username": asset.sshuser, "password": asset.sshpwd, "port": asset.sshport}]
#
#         runner = ANSRunner(resource)
#         runner.run_module([aip], module_name=module, module_args='')
#         if runner.ret == 0:
#             results = runner.get_module_results[0]
#             server_info, server_model, nks = runner.handle_setup_data(results)
#
#             asset.cpu = server_info['cpu_model']
#             asset.logical_cpu = server_info['vcpu_number']
#             asset.ram = server_info['ram_total']
#             asset.disk = server_info['disk_total']
#
#             asset.save()
#             ip = request.META.get('REMOTE_HOST')
#             msg = '更新: %s 硬件信息' % aip
#             save_log.delay(request.user.realname, action='change', resource='Assets资产表', operating=msg, ip=ip)
#             return Response(res)
#         else:
#             # 此时失败了，更新数据库状态
#             asset.is_active = False
#             asset.status = 2
#             asset.save()
#             res["code"] = 400
#             res["msg"] = "ansible执行失败"
#             res["error"] = str(runner.get_module_results[0])
#             return Response(res)


class TestPingView(APIView):
    permission_classes = []

    def get(self, request, **kwargs):
        """
        测试联通性的
        :param request:
        :param id:
        :return: HttpResponse  ok or no
        """
        res = {"code": 200, "msg": None}
        v = request.GET.get("v", 1)
        asset = get_object_or_404(Assets, id=self.kwargs.get("id", None))
        ip = asset.ip
        ping = False
        port_check = False
        account_check = False
        msg = None
        if v == "1":
            try:
                out = subprocess.check_output(["fping", ip], universal_newlines=True, stderr=subprocess.STDOUT,
                                              timeout=10)
            except subprocess.CalledProcessError as e:
                out = e.stdout
            except subprocess.TimeoutExpired as e:
                out = "Time out!" + e.stdout
            if "alive" in out:
                ping = True
            elif "unreachable" in out:
                msg = "服务器不可达: <br>" + out
            elif "Time" in out:
                msg = "Ping服务器超时:" + out
            else:
                msg = "主机无法Ping通:"

            # 成功了更新下数据库
            if ping:
                asset.is_pass = 1
                asset.status = 1
                asset.save()
            else:
                # 成功了更新下数据库
                asset.is_pass = 0
                asset.status = 2
                asset.unicom_note = msg
                asset.save()


        elif v == "2":
            # 使用telnetlib 连接端口
            try:
                tb = telnetlib.Telnet(ip, asset.sshport, timeout=4)
            except TimeoutError:
                msg = "端口连接超时"
            except OSError as e:
                msg = "失败:" + str(e)
            else:
                port_check = True
                tb.close()

            # 成功了更新下数据库
            if port_check:
                asset.is_pass = 1
                asset.status = 1
                asset.save()
            else:
                # 成功了更新下数据库
                asset.is_pass = 2
                asset.status = 2
                asset.unicom_note = msg
                asset.save()
        elif v == "3":
            ssh = SSHClient()
            ssh.set_missing_host_key_policy(AutoAddPolicy())
            try:
                ssh.connect(hostname=asset.ip, username=asset.sshuser, port=int(asset.sshport),
                            password=asset.sshpwd, timeout=10)

            except Exception as e:
                msg = " 账户连接失败:" + str(e)
            else:
                ssh.close()
                account_check = True

            # 成功了更新下数据库
            if account_check:
                asset.is_pass = 1
                asset.status = 1
                asset.save()
            else:
                # 成功了更新下数据库
                asset.is_pass = 2
                asset.status = 2
                asset.unicom_note = msg
                asset.save()
        # 返回
        if ping or account_check or port_check:
            res["msg"] = ip
            return Response(res)
        else:
            res["code"] = 400
            res["msg"] = msg
            return Response(res)


class GetUserAssetsView(APIView):
    permission_classes = []

    def get(self, request, **kwargs):
        ip = request.GET.get("ip", None)
        if request.user.is_superuser:
            # 表示有Ip过率
            if ip:
                assets = Assets.objects.only("id", "ip").filter(ip__contains=ip)
            else:
                assets = Assets.objects.only("id", "ip").all()
            result = []
            for asset in assets:
                s = {}
                s["id"] = str(asset.id)
                s["name"] = asset.ip
                result.append(s)
            return Response(result)
        else:
            user = request.user
            result = []
            # 查询出该用户项目下的资产
            projs = Project.objects.filter(Q(auth_users=user) | Q(creator=user)) \
                .prefetch_related("auth_users").select_related("creator")
            for proj in projs:
                if ip:
                    assets = Assets.objects.filter(project=proj, ip__contains=ip)
                else:
                    assets = Assets.objects.filter(project=proj)
                for asset in assets:
                    s = {}
                    s["id"] = str(asset.id)
                    s["name"] = asset.ip
                    result.append(s)
            return Response(result)
