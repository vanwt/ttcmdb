import re
from queue import Queue
from . import parser, controller


class BaseCmdString(object):
    PARSER_FUNCS = []
    CONTROL_CLASS = []

    def __int__(self):
        self.cmd = ""
        self.cmd_now = ""
        self.source = ""
        self.pipeline = None
        self.pointer = -1

    def _renew__init__(self):
        self.cmd = ""
        self.cmd_now = ""
        self.pipeline = None
        self.pointer = -1

    def ready(self, source):
        self._renew__init__()
        self.source = repr(source).strip("'")
        self.pipeline_operation()

    def pipeline_operation(self):
        self.pipeline = Queue()
        cmd = self.source.split("\\x")
        for item in cmd:
            for parse in self.PARSER_FUNCS:
                if parse.filter(work=self.pipeline, item=item):
                    break
                else:
                    continue
            else:
                self.pipeline.put(item)

    # 指针左移
    def pointer_left(self):
        if self.pointer <= -1:
            return False
        self.pointer -= 1

    # 指针右移
    def pointer_right(self):
        if self.pointer >= len(self.source) - 1:
            return
        self.pointer += 1

    def input_text(self, text):
        begin = self.cmd[:self.pointer + 1]
        end = self.cmd[self.pointer + 1:]
        self.cmd = begin + text + end
        # 添加了几个，指针位移几次
        for i in range(len(text)):
            self.pointer_right()


class CmdTOString(BaseCmdString):
    PARSER_FUNCS = [parser.CursorParse(), parser.DeleteParse()]
    CONTROL_CLASS = [controller.BackspaceController(),
                     controller.Cursor_D_Controller(),
                     controller.Cursor_C_Controller()]

    def worker(self, source):
        self.ready(source=source)
        self.action()
        return self.cmd

    def action(self):
        # 循环处理
        while not self.pipeline.empty():
            self.cmd_now = self.pipeline.get()
            for control in self.CONTROL_CLASS:
                if control.has_attr(self.cmd_now):
                    control.splice(source=self)
                    break
            else:
                self.input_text(self.cmd_now)


if __name__ == '__main__':
    cmd_string = CmdTOString()
    cmd = "uptime \x7f\x7fe\x1b[D\x1b[D\x1b[Dddd\x1b[C\x1b[C\x1b[Caaa\x7f\x7f\x7f\x7f\x7f\x7f\x7f\x7f\x7fime"
    cmd_string.worker(cmd)
    print(cmd_string.cmd)
    cmd = 'ifconfig \x7f\x7f\x7f\x7f456\x1b[D\x1b[D\x1b[D\x1b[D\x1b[D789\x1b[C\x1b[C\x1b[C45\x1b[D\x1b[D\x1b[D\x1b[D\x1b[D\x1b[D\x1b[D\x1b[D\x1b[Dbbb\x1b[C\x1b[C\x1b[C\x1b[C\x1b[C\x1b[C\x1b[C\x1b[C\x1b[C\x1b[C\x1b[C\x7f\x7f\x7f\x7f\x7f\x7f\x7f\x7f\x7f\x1b[D\x1b[D\x1b[Dss\x1b[D\x1b[D\x1b[D\x1b[Dcon\x1b[C\x1b[C\x1b[C\x1b[C\x1b[C\x1b[C\x1b[Cfig\x1b[D\x1b[D\x1b[D\x7f\x7f\x7f\x7f\x7f\x7f\x7f\x1b[C\x1b[C\x1b[C'
    cmd_string.worker(cmd)
    print(cmd_string.cmd)

