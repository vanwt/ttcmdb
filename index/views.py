from django.views.generic import TemplateView, View
from django.shortcuts import render, HttpResponse
from user.models import User
from assets.models import Assets
from log.models import OperatingLog
from django.contrib.sessions.models import Session
from datetime import datetime
from webssh.models import SessionLog


# Create your views here.


class IndexView(TemplateView):
    template_name = 'index/index.html'

    def get_context_data(self, **kwargs):
        # 获取在线人数
        online = Session.objects.filter(expire_date__gte=datetime.now()).count()
        # 历史记录管理员看所有，普通用户只能看自己的
        if self.request.user.is_superuser:
            opera = OperatingLog.objects.only('operating', 'create_time').all().order_by('-create_time').values()[0:5]
        else:
            opera = OperatingLog.objects.only('operating', 'create_time').filter(
                user=self.request.user.username).order_by('-create_time').values()[0:5]

        context = super(IndexView, self).get_context_data(**kwargs)
        context.update({
            "user_count": User.get_nums(),
            "session_count": SessionLog.objects.filter(status=1).only('id').count(),
            "assets_count": Assets.get_nums(),
            "operating_log": opera,
            "server_data": Assets.get_string_servers(),
            "online": online,
        })
        return context
