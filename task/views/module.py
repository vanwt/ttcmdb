import json
from django.shortcuts import render, HttpResponse
from django.views.generic import View, DetailView
from assets.models import Assets
from django_filters.views import FilterView
from ..models import AnsibleModuleLog
from ..filters import ModuleLogFilter


# Create your views here.
class RunAnsModule(View):
    """
        执行模块的接口，前端使用ajax
        get方法返回页面和主要信息
    """
    template_name = 'task/module/run_module.html'

    def get(self, request, **kwargs):
        hosts_list = Assets.objects.only('id', 'ip').all()
        return render(request, self.template_name, {"hosts_list": hosts_list})

    def post(self, request, **kwargs):
        """
        检查命令，执行ansible
        :param request:
        :param kwargs:
        :return:
        """
        try:

            response = {
                "code": 200,
                "result": None,
            }

        except Exception as e:
            response = {
                "code": 500,
                "result": "致命错误，请检查配置参数！%s" % e
            }

        return HttpResponse(json.dumps(response))


class AnsModuleLogView(FilterView):
    """
     显示执行模块记录表的视图
    """
    template_name = 'task/module/module_log.html'
    filterset_class = ModuleLogFilter
    queryset = AnsibleModuleLog.objects.all().select_related("ans_user")


class AnsModuleLogInfoView(DetailView):
    """
         展示日志详细信息的视图
    """
    template_name = 'task/module/run-module-info.html'
    context_object_name = 'module'
    model = AnsibleModuleLog
    pk_url_kwarg = 'id'
