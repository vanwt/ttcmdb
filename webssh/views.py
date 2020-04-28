"""
2019 5.6
    客户访问流程
    首先经过视图clientView 然后查询出配置信息，查询配置使用ajax 调用get_server_attributes 接口
    然后在页面点击连接，后首先会发送post请求，这时候生成一个key并存入数据库 SessionLog表，此key伴随连接结束
    存入数据库后，向前端返回状态码200 和生成的key ,前端200后，用get请求访问连接，要携带这个key，没有key则404 然后通过websocket发送请求
    每次的websocket交互必须有此key，
"""
from django.shortcuts import render
from django.views.generic import View, ListView, DetailView
from .models import SessionLog, CodeLog
from django_filters.views import FilterView
from .filters import SSHLogFilter


# Create your views here.

class ClientView(View):
    def get(self, request, **kwargs):
        return render(request, 'webssh/index.html')


class SessionListView(ListView):
    template_name = 'webssh/session_online_log.html'
    context_object_name = 's_l'

    def get_queryset(self):
        if self.request.user.is_superuser:
            return SessionLog.objects.filter(status=1)
        else:
            return SessionLog.objects.filter(status=1, user=self.request.user.realname)


# 已经执行完成的会话列表
class SessionLogView(FilterView):
    template_name = 'webssh/session_log.html'
    filterset_class = SSHLogFilter

    def get_queryset(self):
        """
         超级用户：返回所有记录
         普通用户：返回这个用户的记录
        :return:
        """
        if self.request.user.is_superuser:
            return SessionLog.get_all()
        else:
            return SessionLog.get_all_by_user(self.request.user)


class ConnectionLogInfoView(DetailView):
    model = SessionLog
    pk_url_kwarg = "id"
    template_name = "webssh/connection_detail.html"
    context_object_name = "connection_log"

    def get_context_data(self, **kwargs):
        obj = self.get_object()
        content = super().get_context_data(**kwargs)
        code_logs = CodeLog.objects.filter(connection=obj).select_related("connection").order_by("addtime")
        content.update({"code_logs": code_logs})
        return content
