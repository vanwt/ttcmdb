from ansible.plugins.callback import CallbackBase
import json


class ModelResultCallback(CallbackBase):
    def __init__(self, *args, **kwargs):
        super(ModelResultCallback, self).__init__(*args, **kwargs)
        self.host_ok = {}
        self.host_unreachable = {}
        self.host_failed = {}

    def v2_runner_on_unreachable(self, result):
        self.host_unreachable[result._host.get_name()] = result

    def v2_runner_on_ok(self, result, *args, **kwargs):
        self.host_ok[result._host.get_name()] = result

    def v2_runner_on_failed(self, result, *args, **kwargs):
        self.host_failed[result._host.get_name()] = result


class ResultCallback2(CallbackBase):
    """用于执行操作的示例回调插件作为结果进入
     如果要将所有结果收集到单个对象中以进行处理
     执行结束，考虑使用``json``回调插件
     或编写自己的自定义回调插件
    """

    def __init__(self, sock=None, *args, **kwargs):
        self.sock = sock
        super(ResultCallback2, self).__init__(*args, **kwargs)

    def v2_runner_on_unreachable(self, result):
        if 'msg' in result._result:
            data = '<code style="color: #FF0000">{host} | unreachable | rc={rc} >> <br>{stdout}<br></code>'.format(
                host=result._host.name, rc=result._result.get('rc'),
                stdout=result._result.get('msg').encode().decode('utf-8'))
        else:
            data = '<code style="color: #FF0000">{host} | unreachable >> <br>{stdout}<br></code>'.format(
                host=result._host.name,
                stdout=json.dumps(result._result, indent=4))

        self.send_callback(data)

    def v2_runner_on_ok(self, result, *args, **kwargs):
        if 'rc' in result._result and 'stdout' in result._result:
            data = '<code style="color: #008000">{host} | success | rc={rc} >> <br>{stdout}<br></code>'.format(
                host=result._host.name, rc=result._result.get('rc'),
                stdout=result._result.get('stdout'))
        elif 'results' in result._result and 'rc' in result._result:
            data = '<code style="color: #008000">{host} | success | rc={rc} >> <br>{stdout}\n</code>'.format(
                host=result._host.name, rc=result._result.get('rc'),
                stdout=result._result.get('results')[0])
        elif 'module_stdout' in result._result and 'rc' in result._result:
            data = '<code style="color: #008000">{host} | success | rc={rc} >> <br>{stdout}<br></code>'.format(
                host=result._host.name, rc=result._result.get('rc'),
                stdout=result._result.get('module_stdout').encode().decode('utf-8'))
        else:
            data = '<code style="color: #008000">{host} | success >> <br>{stdout}<br></code>'.format(
                host=result._host.name,
                stdout=json.dumps(result._result, indent=4))

        self.send_callback(data)

    def v2_runner_on_failed(self, result, *args, **kwargs):
        if 'stderr' in result._result:
            data = '<code style="color: #FF0000">{host} | failed | rc={rc} >> <br>{stdout}<br></code>'.format(
                host=result._host.name,
                rc=result._result.get('rc'),
                stdout=result._result.get('stderr').encode().decode('utf-8'))
        elif 'module_stdout' in result._result:
            data = '<code style="color: #FF0000">{host} | failed | rc={rc} >> <br>{stdout}<br></code>'.format(
                host=result._host.name,
                rc=result._result.get('rc'),
                stdout=result._result.get('module_stdout').encode().decode('utf-8'))
        else:
            data = '<code style="color: #FF0000">{host} | failed >> <br>{stdout}<br></code>'.format(
                host=result._host.name,
                stdout=json.dumps(result._result, indent=4))

        self.send_callback(data)

    def send_callback(self, data):
        if self.sock:
            self.sock.send(data)


class ResultCallback(CallbackBase):
    """A sample callback plugin used for performing an action as results come in

    If you want to collect all results into a single object for processing at
    the end of the execution, look into utilizing the ``json`` callback plugin
    or writing your own custom callback plugin
    """

    def __init__(self, json=False, sock=None, *args, **kwargs):
        self.json = json
        self.msg = None
        self.sock = sock
        super(ResultCallback, self).__init__(*args, **kwargs)

    def v2_runner_on_ok(self, result, **kwargs):
        """Print a json representation of the result

        This method could store the result in an instance attribute for retrieval later
        """
        host = result._host
        msg = json.dumps({host.name: result._result}, indent=4)
        self.msg = msg
        print(msg)
        self.send_callback(msg)

    def send_callback(self, data):
        if self.sock:
            self.sock.send(data)


# 格式化callback类
class PlayBookResultCallback(CallbackBase):
    CALLBACK_VERSION = 2.0

    def __init__(self, sock=None, is_json=False, *args, **kwargs):
        """"""
        self.is_json = is_json
        self.sock = sock
        self.task_ok = {}
        self.task_skipped = {}
        self.task_failed = {}
        self.task_status = {}
        self.task_unreachable = {}
        super(PlayBookResultCallback, self).__init__(*args, **kwargs)

    def v2_playbook_on_play_start(self, play):
        if not self.is_json:
            name = play.get_name().strip()
            if not name:
                msg = '<code style="color: #0000CD">\nPLAY {}\n</code>'.format('*' * 100)
            else:
                msg = '<code style="color: #0000CD">\nPLAY [{}] {}\n</code>'.format(name, '*' * 100)
            self.send_callback(msg)

    def v2_playbook_on_task_start(self, task, is_conditional):
        if not self.is_json:
            msg = '<code style="color: #0000CD">\nTASK [{}] {}\n</code>'.format(task.get_name(), '*' * 100)
            self.send_callback(msg)

    def v2_runner_on_ok(self, result, *args, **kwargs):
        if not self.is_json:
            # 正常的输出模式
            if result.is_changed():
                data = '<code style="color: #B8860B">[{}]=> changed\n</code>'.format(result._host.name)
            else:
                data = '<code style="color: #008000">[{}]=> ok\n</code>'.format(result._host.name)
            self.send_callback(data)
        else:
            # json 格式
            self.task_ok[result._host.get_name()] = result

    def v2_runner_on_failed(self, result, *args, **kwargs):

        if not self.is_json:
            # out
            data = '<code style="color: #FF0000">[{}]=> {}: {}\n</code>'.format(result._host.name, 'failed',
                                                                                self._dump_results(result._result))
            self.send_callback(data)
        else:
            # json 格式
            self.task_failed[result._host.get_name()] = result

    def v2_runner_on_unreachable(self, result):
        if not self.is_json:
            # out
            data = '<code style="color: #FF0000">[{}]=> {}: {}\n</code>'.format(result._host.name, 'unreachable',
                                                                                self._dump_results(result._result))
            self.send_callback(data)
        else:
            # json
            self.task_unreachable[result._host.get_name()] = result

    def v2_runner_on_skipped(self, result):
        if not self.is_json:
            data = '<code style="color: #FFFF00">[{}]=> {}: {}\n</code>'.format(result._host.name, 'skipped',
                                                                                self._dump_results(result._result))
            self.send_callback(data)
        else:
            # json
            self.task_ok[result._host.get_name()] = result

    def v2_playbook_on_stats(self, stats):
        if not self.is_json:
            hosts = sorted(stats.processed.keys())
            data = '<code style="color: #8A2BE2	">\nPLAY RECAP {}\n'.format('*' * 100)
            self.send_callback(data)
            for h in hosts:
                s = stats.summarize(h)
                msg = '<code style="color: #8A2BE2">{} : ok={} changed={} unreachable={} failed={} skipped={}\n</code>'.format(
                    h, s['ok'], s['changed'], s['unreachable'], s['failures'], s['skipped'])
                self.send_callback(msg)
        else:
            hosts = sorted(stats.processed.keys())
            for h in hosts:
                t = stats.summarize(h)
                self.task_status[h] = {
                    "ok": t['ok'],
                    "changed": t['changed'],
                    "unreachable": t['unreachable'],
                    "skipped": t['skipped'],
                    "failed": t['failures']
                }

    def send_callback(self, data):
        if self.sock:
            self.sock.send(data)
