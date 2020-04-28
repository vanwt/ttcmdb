import shutil
import multiprocessing
from ansible import constants
from ansible.parsing.dataloader import DataLoader
from ansible.playbook.play import Play
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.module_utils.common.collections import ImmutableDict
from ansible.executor.playbook_executor import PlaybookExecutor
from ansible.inventory.manager import InventoryManager
from ansible.vars.manager import VariableManager
from ansible import context
import ansible.constants as C
from .callback import PlayBookResultCallback, ResultCallback, ResultCallback2
from .get_server_info import HostGenerate


class MyTaskQueueManager(TaskQueueManager):
    def _initialize_processes(self, num):
        self._workers = []
        current_process = multiprocessing.current_process
        deamon_my = current_process()._config['daemon'] = False
        for i in range(num):
            relt_q = multiprocessing.Queue()
            self._workers.append([None, relt_q])


class MyInventory:
    def __init__(self, resource, source=None):
        self.resource = resource
        self.loader = DataLoader()

        self.inventory = InventoryManager(loader=self.loader, sources=source)
        self.variable_manager = VariableManager(loader=self.loader, inventory=self.inventory)
        self.dynamic_resource()

    def add_group(self, hosts, group_name):
        # 添加组
        self.inventory.add_group(group_name)

        for host in hosts:
            hostip = host.get('host')
            hostport = host.get("port")
            username = host.get("username")
            password = host.get("password")

            # 必须是已有的组
            # print("添加组", hostip, group_name)
            self.inventory.add_host(hostip, group_name)
            # 添加到ansible主机变量，ansible自身调用
            self.inventory.get_host(hostip).set_variable('ansible_ssh_ip', hostip)
            self.inventory.get_host(hostip).set_variable('ansible_ssh_port', hostport)
            self.inventory.get_host(hostip).set_variable('ansible_ssh_user', username)
            self.inventory.get_host(hostip).set_variable('ansible_ssh_pass', password)
            # 老版本
            self.inventory.get_host(hostip).set_variable('ansible_ip', hostip)
            self.inventory.get_host(hostip).set_variable('ansible_port', hostport)
            self.inventory.get_host(hostip).set_variable('ansible_user', username)
            self.inventory.get_host(hostip).set_variable('ansible_pass', password)
            # 管理员密码
            self.inventory.get_host(hostip).set_variable('ansible_sudo_pass', password)

            # add to group
            self.inventory.add_host(host=hostip, group=group_name, port=hostport)

    def dynamic_resource(self):
        if isinstance(self.resource, list):
            self.add_group(self.resource, "all")
        elif isinstance(self.resource, dict):
            self.resource = [self.resource]
            self.add_group(self.resource, "all")


class ANSRunnser:
    def __init__(self, resource=None, **kwargs):
        self.resource = resource
        self.loader = DataLoader()
        self.callback = None
        self.passwords = {}
        self.results_raw = {}
        self.tqm = None
        invent = MyInventory(self.resource)
        self.inventory = invent.inventory
        self.variable_manager = invent.variable_manager
        #  判断有没有设置执行参数
        self._is_set_config = False

    def set_context(self, **config):

        if self._is_set_config:
            return None

        self._is_set_config = True

        # 先初始化所需要的参数
        skip_tags = config.get("skip_tags", [])
        tags = config.get("tags", [])
        become_user = config.get("become_user", None)
        become_method = config.get("become_method", None)
        extra_vars = config.get("extra_vars", tuple())
        # 设置ansible content上下文
        # 此处extar_var 在动态生成主机组的时候添加

        context.CLIARGS = ImmutableDict(connection='local',
                                        forks=10,
                                        become=None,
                                        module_path=None,
                                        verbosity=5,
                                        become_method=become_method,
                                        become_user=become_user,
                                        check=False,
                                        diff=False,
                                        syntax=False,
                                        start_at_task=None,
                                        skip_tags=skip_tags,
                                        tags=tags,
                                        extra_vars=extra_vars
                                        )

    def run_playbook(self, playbook_path=None, sock=None, **data):
        # 设置ansile全局变量
        if self._is_set_config:
            self.set_context(**data)
        # 执行参数

        # 设置回调为playbook
        self.callback = PlayBookResultCallback(sock=sock)

        executor = PlaybookExecutor(
            playbooks=[playbook_path],
            inventory=self.inventory,
            variable_manager=self.variable_manager,
            loader=self.loader,
            passwords=self.passwords
        )
        executor._tqm._stdout_callback = self.callback
        # 关闭第一次使用ansible连接客户端是输入命令
        constants.HOST_KEY_CHECKING = False
        # 执行
        result = executor.run()
        print(result)

    def run_module(self, host_list, module_name, module_args, sock=None, json=False):
        """
        执行模块
        """
        print(module_name, module_args)
        # 定义返回的执行类
        if not type(host_list) is str:
            print("执行hosts必须是字符串")
            return
        self.callback = ResultCallback(sock=sock, json=json)  # sock=sock
        # 这也将自动从play_source中提供的信息创建任务对象

        play_source = dict(
            name="Ansible Play",
            hosts=host_list,
            gather_facts='no',
            tasks=[
                dict(
                    action=dict(
                        module=module_name,
                        args=module_args
                    ),
                    register="shell_out")
            ]
        )

        # 创建播放对象，playbook对象使用.load而不是init或new方法，
        play = Play().load(play_source, variable_manager=self.variable_manager, loader=self.loader)
        # print('运行命令', module_args)
        # 实际上运行tqm
        ret = None
        try:
            self.tqm = TaskQueueManager(
                inventory=self.inventory,
                variable_manager=self.variable_manager,
                loader=self.loader,
                passwords=self.passwords,
                stdout_callback=self.callback,
            )
            # 关闭第一次使用ansible连接客户端时输入命令
            constants.HOST_KEY_CHECKING = False
            ret = self.tqm.run(play)
        except Exception as e:
            print('error：%s' % e)
        finally:
            if self.tqm is not None:
                self.tqm.cleanup()
            # 清除执行缓存
            shutil.rmtree(C.DEFAULT_LOCAL_TMP, True)
        return ret

    def get_playbook_result(self):
        self.results_raw = {'skipped': {}, 'failed': {}, 'ok': {}, "status": {}, 'unreachable': {}, "changed": {}}
        for host, result in self.callback.task_ok.items():
            if not isinstance(result, dict):
                self.results_raw['ok'][host] = result._result

        for host, result in self.callback.task_failed.items():
            if not isinstance(result, dict):
                self.results_raw['failed'][host] = result._result

        for host, result in self.callback.task_status.items():
            self.results_raw['status'][host] = result

        for host, result in self.callback.task_skipped.items():
            if not isinstance(result, dict):
                self.results_raw['skipped'][host] = result._result

        for host, result in self.callback.task_unreachable.items():
            if not isinstance(result, dict):
                self.results_raw['unreachable'][host] = result._result
        return self.results_raw


if __name__ == '__main__':
    resource = {
        "host": "localhost",
        "username": "root",
        "password": "xinshang123",
        "port": "22",
    }
    # resource = HostGenerate(hosts)
    ans = ANSRunnser(resource)

    ans.set_context()
    # ans.run_playbook("/home/test.yml")
    ans.run_module("localhost", "command", "uptime")
    # result = ans.get_module_results()
    # print(result)
