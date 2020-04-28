from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.db.utils import IntegrityError
from assets.models import Assets, SystemUser
from .models import SessionLog


# 用于接受页面传递的Id查询出服务器详细的信息


class GetAssetSystemUserView(APIView):
    def post(self, request, **kwargs):
        result = {"ip": None, "port": 22, "users": [], "id": None}
        # 获取所选服务器
        id = request.data.get('sid', None)
        asset = get_object_or_404(Assets, id=id)
        users = [{"id": u.id, "username": u.username} for u in asset.system_users.all()]
        # 查询出该主机推送过的所有用户，没有就显示root
        if request.user.is_superuser:
            users += [{"id": "0", "username": "root"}]
        result["id"] = asset.id
        result["users"] = users
        return Response(result, status=200)


class MakeLinkView(APIView):
    def post(self, request, **kwargs):
        sid = request.data.get('sid', None)
        uid = request.data.get('uid', None)
        # 先判断有没有这个资产
        asset = get_object_or_404(Assets, id=sid)

        if uid == '0':
            # 如果等于0 表示使用root用户登录
            sshuser = "root"
        else:
            sshuser = get_object_or_404(SystemUser, id=uid).username
        try:
            # 存入连接日志
            sl = SessionLog()
            sl.user = request.user.realname
            sl.host = asset.ip
            # 状态1 是会话连接中
            sl.ssh_user = sshuser
            sl.save()
        except IntegrityError:
            return Response({"code": 200, "msg": "连接生成失败，请重新尝试"})
        # 返回的key 是当前连接生成的key,每次连接都不一样，sid用于查询主机 在customer.py中
        return Response({"code": 200, "key": str(sl.id), "sid": sid, "uid": uid})
