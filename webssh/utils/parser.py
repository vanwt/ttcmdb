from abc import ABCMeta, abstractmethod
import re


class BaseParseClass(metaclass=ABCMeta):

    @abstractmethod
    def filter(self, work, item):
        return True


class DeleteParse(BaseParseClass):
    def filter(self, work, item):
        if not "7f" == item[:2]:
            return False
        work.put(item[:2])

        if item[2:] == "":
            return True
        work.put(item[2:])
        return True


class CursorParse(BaseParseClass):
    def filter(self, work, item):
        compile = re.compile(r"1b\[[A-D]")
        find = compile.search(item)
        if not find:
            return False
        work.put(item[:4])

        if item[4:] == "":
            return True

        work.put(item[4:])
        return True
