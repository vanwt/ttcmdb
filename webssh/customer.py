from channels.generic.websocket import WebsocketConsumer
import json
from .utils.wstty import SSHTty
from django.http.request import QueryDict
from assets.models import Assets, SystemUser
from .models import SessionLog
from datetime import datetime
from threading import Thread


class SSHClient(WebsocketConsumer):
    message = {'status': 0, 'message': None, "key": None}
    """
    status:
        0: ssh 连接正常, websocket 正常
        1: 发生未知错误, 关闭 ssh 和 websocket 连接

    message:
        status 为 1 时, message 为具体的错误信息
        status 为 0 时, message 为 ssh 返回的数据, 前端页面将获取 ssh 返回的数据并写入终端页面
    """

    def connect(self):
        # 接受连接

        self.accept()

        # 获取参数 进行验证
        qs = self.scope['query_string']
        argv = QueryDict(query_string=qs, encoding='utf-8')

        # 获取服务器id 及 用户id,记录id
        asset_id = argv.get('sid', None)
        uid = argv.get("uid", None)
        session_id = argv.get("key", None)
        user_key = argv.get("key2", None)

        # 查询值
        asset = Assets.get_by_id(asset_id)
        self.connection = SessionLog.get_by_id(session_id)
        if not self.connection or self.connection.used:
            self.send("连接拒绝")
            self.close()

        # 先判断是否是管理员,不是管理员一律使用uuser_key  判断用户是用user_key 还是密码
        print(1)
        # 建立ssh连接
        if uid == '0':
            # 0 用root默认用户登录
            self.ssh = SSHTty(asset, self, is_user=False, connection_obj=self.connection)
        else:
            login_user = SystemUser.get_by_id(uid)
            if login_user is None:
                self.close()
            # 传入用户名密码
            self.ssh = SSHTty(asset, self, is_user=True, user=login_user.username, pwd=login_user.password,
                              connection_obj=self.connection)
        print(2)
        # 开始
        print(self.ssh.connection)
        self.ssh.connect()
        print(3)

        # 开启线程，监控服务器,每当服务器有消息是发送给ws
        Thread(target=self.ssh.server_to_ws).start()
        print(4)

    def disconnect(self, code):
        try:
            # 存日志连接记录
            self.ssh.close()
            self.connection.status = 0
            self.connection.used = True
            self.connection.end_time = datetime.now()
            self.connection.save()
            # 传递session
        except Exception as e:
            print(e)
        finally:
            try:
                self.close()
                self.ssh.close()
            except:
                pass

    def receive(self, text_data=None, bytes_data=None):
        self.ssh.ws_to_server(text_data)
