import json
from django.http import JsonResponse
from django.views.generic import View
from ..models import  Log_Cron
from django_filters.views import FilterView
from ..filters import LogFilter


class LogListView(FilterView):
    template_name = 'plan/log-list.html'
    ordering = '-id'
    model = Log_Cron
    filterset_class = LogFilter


class LogDelView(View):
    @staticmethod
    def post(request):
        ret = {'code': 200, 'error': None, }
        try:
            if request.POST.get('id'):
                id = request.POST.get('id', None)
                Log_Cron.objects.get(id=id).delete()
        except Exception as e:
            ret['code'] = 400
            ret['error'] = '删除请求错误{}'.format(e)
        else:
            return JsonResponse(ret)
