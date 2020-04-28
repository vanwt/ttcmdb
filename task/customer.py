import json, os
from channels.generic.websocket import WebsocketConsumer
from datetime import datetime
from common.ansible_api.get_server_info import HostGenerate
from common.ansible_api.ansible_api_v1 import ANSRunnser
from .models import AnsiblePlaybook, RunRoleScript
from ttcmdb.settings import BASE_DIR, ANSIBLE_ROLE_PATH
from assets.models import Assets


class PlaybookConsumer(WebsocketConsumer):
    message = {'status': 0, 'message': None, "key": None}
    """
    status:
        0: ssh 连接正常, websocket 正常
        1: 发生未知错误, 关闭 ssh 和 websocket 连接

    message:
        status 为 1 时, message 为具体的错误信息
        status 为 0 时, message 为 ssh 返回的数据, 前端页面将获取 ssh 返回的数据并写入终端页面
    """

    def __init__(self, *args, **kwargs):
        super(PlaybookConsumer, self).__init__(*args, **kwargs)
        self.ans_info = None

    def connect(self):
        # 接受连接
        # 从这里执行ansible playbook
        # 把self传递到ansible playbook中

        self.accept()

    def disconnect(self, code):
        pass

    def receive(self, text_data=None, bytes_data=None):
        # 这是接受web过来的消息
        self.ans_info = json.loads(text_data)
        # 获取参数
        ids = self.ans_info['ids']
        id = self.ans_info['id']
        is_role = self.ans_info["role"]
        print(ids)
        if ids == [] and not id and is_role:
            # 如果没有者两个值 断开连接
            self.send("无效的参数，断开连接...")
            self.close()
        # 如果等于0 表示是playbook
        if is_role == 0:
            self.send("正在执行剧本...")
            # 运行
            self.run_playbook(ids, id)
        else:
            self.send("正在执行Role...")
            self.run_role(ids, id)

    def run_playbook(self, ids, pid):
        """
        playbook 的
        :param ids:
        :param pid:
        :return:
        """
        try:
            # 查询出要执行的剧本
            pb = AnsiblePlaybook.objects.only("playbook_content", "playbook_name").get(id=pid)

            # 生成路径
            name = datetime.now().strftime("%Y%m%d-%H%M%S") + ".yml"
            dir = os.path.join(BASE_DIR, "static", "playbooks", "run", name)

            # 从数据库读取，写入到临时文件
            with open(dir, "w") as f:
                f.write(pb.playbook_content)
                f.close()

            # 生成主机组
            resource = HostGenerate(ids)

            ans = ANSRunnser(resource=resource)
            ans.set_context(become_method='sudo', become_user='root')
            # 要传路径和 当前对象 ，用于发送callback
            ans.run_playbook(playbook_path=dir, sock=self)
        except Exception as e:
            print("执行playbook报错:", e)
            self.send("执行playbook报错:" + str(e))
        finally:
            # 结束
            self.send("执行playbook完成,断开连接...")
            self.close()

    def run_role(self, ids, rid):
        """
        role的
        :param ids:
        :param rid:
        :return:
        """
        try:
            # 查询出要执行的role脚本
            rs = RunRoleScript.objects.only("r_content", "r_name").get(id=rid)

            # 生成路径
            name = datetime.now().strftime("%Y%m%d-%H%M%S") + ".yml"
            dir = os.path.join(ANSIBLE_ROLE_PATH, name)

            # 从数据库读取，写入到临时文件
            with open(dir, "w") as f:
                f.write(rs.r_content)
                f.close()

            # 生成主机组
            resource = HostGenerate(ids)

            # 执行ansible
            ans = ANSRunnser(resource)
            ans.set_context(become_method='sudo', become_user='root')
            # 要传路径和 当前对象 ，用于发送callback
            ans.run_playbook(playbook_path=dir, sock=self)

        except Exception as e:
            print("执行Role报错:", e)
            self.send("执行Role报错:" + str(e))
        finally:
            # 结束
            self.send("执行Role完成,断开连接...")
            self.close()


class RunModuleConsumer(WebsocketConsumer):
    message = {'status': 0, 'message': None, "key": None}
    """
    status:
        0: ssh 连接正常, websocket 正常
        1: 发生未知错误, 关闭 ssh 和 websocket 连接

    message:
        status 为 1 时, message 为具体的错误信息
        status 为 0 时, message 为 ssh 返回的数据, 前端页面将获取 ssh 返回的数据并写入终端页面
    """

    def __init__(self, *args, **kwargs):
        super(RunModuleConsumer, self).__init__(*args, **kwargs)
        self.ans_info = None

    def connect(self):
        # 接受连接
        # 从这里执行ansible run_module

        self.accept()

    def disconnect(self, code):
        pass

    def receive(self, text_data=None, bytes_data=None):
        # 这是接受web过来的消息
        self.ans_info = json.loads(text_data)
        # 获取参数
        ids = self.ans_info['ids']
        args = self.ans_info["args"]
        module = self.ans_info["module"]
        print(ids, args, module)
        try:
            # 生成resource
            resource = HostGenerate(ids)

            # 生成执行时需要的hosts
            print(resource)
            runner = ANSRunnser(resource)
            runner.set_context(become_method='sudo', become_user='root')
            host_list = [host["host"] for host in resource]
            # 执行模块
            ret = runner.run_module(host_list=",".join(host_list), module_name=module, module_args=args, sock=self)
            print(ret)
        except Exception as e:
            print(e)
            self.send("执行Module报错:" + str(e))
        finally:
            # 结束
            self.close()
