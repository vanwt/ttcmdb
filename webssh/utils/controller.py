from abc import abstractmethod, ABCMeta


class BaseController(metaclass=ABCMeta):
    ITEM = ""

    def has_attr(self, item):
        if item == self.ITEM:
            return True
        else:
            return False

    @abstractmethod
    def splice(self, source):
        pass


class BackspaceController(BaseController):
    ITEM = "7f"

    def splice(self, source):
        # 最开端无法删除，直接返回,不费劲了
        if source.pointer == -1:
            return
        try:
            # 把字符串化成列表
            temp = list(source.cmd)
            # 删除指针所在的元素
            del temp[source.pointer]
            # 合并为字符串
            source.cmd = ''.join(temp)
            # 删除后指针左移一位
            source.pointer_left()  # 不要忘记指针左移
        except:
            pass


class Cursor_D_Controller(BaseController):
    ITEM = "1b[D"

    def splice(self, source):
        # 最开端无法删除，直接返回,不费劲了
        if source.pointer == -1:
            return
        # 直接指针左移
        source.pointer_left()


class Cursor_C_Controller(BaseController):
    ITEM = "1b[C"

    def splice(self, source):
        # 最开端无法删除，直接返回,不费劲了
        if source.pointer == -1:
            return
        # 直接指针左移
        source.pointer_right()
