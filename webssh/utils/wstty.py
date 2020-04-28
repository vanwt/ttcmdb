import paramiko
import json
from threading import Thread
import socket
from ..models import SessionLog, CodeLog
from datetime import datetime
from .Cmd_to_string import CmdTOString
import tty
import time
import os
import sys
import select
import termios


class ServerError(Exception):
    """ 定义服务器错误 """
    pass


class Tty(object):
    def __init__(self, asset, sock, is_user=False, user=None, pwd=None, connection_obj=None):
        self.connection = connection_obj  # 连接对象
        self.sock = sock  # 与ws的连接对象
        self.asset = asset
        # 初始化用户名和密码,使用默认值
        self.sshuser = asset.sshuser
        self.sshpwd = asset.sshpwd
        self.ip = None
        self.task = False
        self.data = ""  # 记录总命令
        self.cmd = ""  # 记录累加命令
        self.channel = None
        self.ssh = None
        self.is_commit = False
        self.is_enter = False
        self.log_obj = None
        self.cmd_to_string = CmdTOString()
        # 使用传递的用户密码
        if is_user:
            self.sshuser = user
            self.sshpwd = pwd

    def get_connect(self):
        """ 返回连接成功后的ssh """
        ssh = paramiko.SSHClient()
        ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(paramiko.WarningPolicy)
        try:
            ssh.connect(self.asset.ip, self.asset.sshport, self.sshuser, self.sshpwd, timeout=40)
        except (paramiko.ssh_exception.AuthenticationException, paramiko.ssh_exception.SSHException):
            raise ServerError("认证失败：Authentication Error. ")
        except socket.error:
            raise ServerError('端口可能不对 Connect SSH Socket Port Error, Please Correct it.')
        except TimeoutError:
            raise ServerError("连接超时: Time Out...! ")
        else:
            self.ssh = ssh
            return ssh

    def set_log(self, cmd):
        print("存日志")
        cmd = self.cmd_to_string.worker(cmd)
        if cmd != "":
            self.log_obj = CodeLog()
            self.log_obj.command = cmd
            self.log_obj.connection = self.connection

    def save_log(self, result):
        self.log_obj.result = result
        self.log_obj.save()

    def resize_pty(self, cols, rows):
        # 重新设置窗口大小
        self.channel.resize_pty(width=cols, height=rows)


class SSHTty(Tty):
    def connect(self):
        # 连接ssh
        print(1)
        ssh = self.get_connect()
        print(2)
        # channel = ssh.invoke_shell()
        # 开启隧道
        transport = ssh.get_transport()
        transport.set_keepalive(30)
        transport.use_compression(True)
        print(3)
        # 保持连接
        self.channel = transport.open_session()
        print(4)
        # 开启虚拟终端
        self.channel.get_pty(term='xterm', height=40, width=200)
        self.channel.invoke_shell()
        print(5)

    def close(self):
        """ 需要sessionlog 对象"""
        self.channel.close()
        self.ssh.close()
        self.sock.close()

    def server_to_ws(self):
        while True:
            try:
                x = self.channel.recv(10240).decode("utf-8", "ignore")
                # 使用/t
                if self.is_commit:
                    self.cmd += x
                    self.is_commit = False
                # 使用回车
                elif self.is_enter:
                    if x != "\r\n":
                        self.save_log(x)
                        self.is_enter = False
                elif len(x) == 0:
                    self.sock.send("\r\n*** EOF \r\n")
                    break
                self.sock.send(x)
            except socket.timeout:
                pass

        # 退出循环 主动断开连接
        self.sock.close()

    def ws_to_server(self, press):

        if press != '\r':
            # \t 补全
            if press == "\t":
                self.is_commit = True
            else:
                self.cmd += press
        else:
            # 标记为使用了回车
            if self.cmd != "":
                self.set_log(self.cmd)
                self.cmd = ""
                self.is_enter = True
        if len(press) == 0:
            return False
        self.channel.send(press)

# class SSH:
#     def __init__(self, sock, message):
#         self.sock = sock
#         self.message = message
#
#     def connect(self, host, user, pwd, port=22, timeout=100, term='xterm', pty_width=200, pty_height=40):
#         try:
#             ssh_c = paramiko.SSHClient()
#             ssh_c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#
#             ssh_c.connect(username=user, password=pwd, hostname=host, port=port, timeout=timeout)
#
#             # 建立ssh会话
#             transport = ssh_c.get_transport()
#
#             # 创建一个通道，session用于保持通道的连接
#             self.channel = transport.open_session()
#
#             # 创建pty连接远程服务器，窗口的大小会影响返回的数据
#             # term应该是模拟终端类型的意思?
#             self.channel.get_pty(term=term, width=pty_width, height=pty_height)
#
#             self.channel.invoke_shell()
#
#             # 接受刚打开终端的返回消息，上次登录时间 和一些消息
#             for _ in range(2):
#                 recv = self.channel.recv(2048).decode("utf-8", 'ignore')
#                 self.message['status'] = 0
#                 self.message['message'] = recv
#                 message = json.dumps(self.message)
#
#                 # 发送消息
#                 self.sock.send(message)
#         except socket.timeout as e:
#             self.message['status'] = 1
#             self.message['message'] = '%s连接超时，请检查服务器是否畅通' % e
#             message = json.dumps(self.message)
#             # 设置状态
#             key = self.message.get('key', None)
#             sl = SessionLog.get_by_skey(key)
#             if sl:
#                 sl.user = True
#                 sl.status = 0
#                 sl.end_time = datetime.now()
#                 sl.save()
#             self.sock.send(message)
#             self.sock.close()
#
#     # 关闭连接
#     def close(self):
#         # 当需要断开连接的执行操作
#         self.message['status'] = 1
#         self.message['message'] = '关闭连接'
#         message = json.dumps(self.message)
#
#         # 设置状态
#         key = self.message.get('key', None)
#         sl = SessionLog.get_by_skey(key)
#         if sl:
#             sl.used = True
#             sl.status = 0
#             sl.end_time = datetime.now()
#             sl.save()
#
#         self.sock.send(message)
#         self.channel.close()
#         self.sock.close()
#
#     def django_to_ssh(self, data):
#         try:
#             # data 是从web发送过来的执行命令，是一个字母，多个字母组合成一个命令，
#             # 在经过\r操作(模拟终端上的回车)
#             # 服务器就会返回命令执行的结果了
#             message = data['message']
#             self.channel.send(message)
#             return
#         except Exception as e:
#             print('执行命令错误', e)
#             key = self.message.get('key', None)
#             sl = SessionLog.get_by_skey(key)
#             if sl:
#                 sl.used = True
#                 sl.status = 0
#                 sl.end_time = datetime.now()
#                 sl.save()
#             self.close()
#
#     def django_to_websocket(self):
#         try:
#             while True:
#                 # 等待接受服务器返回的参数
#                 data = self.channel.recv(1024)
#                 try:
#                     data = data.decode("utf-8", 'ignore')
#                 except UnicodeDecodeError:
#                     print("向客户端发送时unicode解码失败...尝试gbk编码")
#                     data = data.decode("gb2312", 'ignore')
#                 # 接受到服务器的消息是str格式的字符串
#                 if not len(data):
#                     return
#                 self.message['status'] = 0
#                 self.message['message'] = data
#                 # 打包服务器的返回值，然后发送给websocket客户端，状态是执行成功的
#                 message = json.dumps(self.message)
#                 self.sock.send(message)
#
#         except Exception as e:
#             print('向客户端发送时报错:', e)
#             key = self.message.get('key', None)
#             sl = SessionLog.get_by_skey(key)
#             if sl:
#                 sl.used = True
#                 sl.status = 0
#                 sl.end_time = datetime.now()
#                 sl.save()
#             self.close()
#
#     def shell(self, data):
#         # 开启两个线程， 一个是向服务器发送命令(单个字母)
#         Thread(target=self.django_to_ssh, args=(data,)).start()
#         # 用来接受服务器返回的参数,服务器没有收到 \r(模拟终端的回车) 是不会返回任何的
#         Thread(target=self.django_to_websocket).start()
#
#     def resize_pty(self, cols, rows):
#         # 重新设置窗口大小
#         self.channel.resize_pty(width=cols, height=rows)
