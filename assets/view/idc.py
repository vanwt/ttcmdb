import django
import json
from django.shortcuts import HttpResponse
from django.views.generic import ListView
from django.db.models import Q
from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator
from ..models import IDC
# from logger.tasks import save_log


class IDCListView(ListView):
    """
    IDC资产表，用于添加IDC 和删除IDC
    """
    template_name = 'assets/IDC.html'
    paginate_by = 10
    model = IDC
    context_object_name = 'idc_list'
    ordering = 'id'

    def post(self, request, **kwargs):
        name = request.POST.get('name')
        linkman = request.POST.get('linkman')
        linkphone = request.POST.get('linkphone')
        address = request.POST.get('address')
        operator = request.POST.get('operator')
        network = request.POST.get('network_segment')
        idc_type = request.POST.get('type')
        band = request.POST.get('bandwidth')

        if band == '':
            print(1)
        if name == '' or linkman == '' or linkphone == '' or address == '' or network == '':
            return HttpResponse('请填写全部内容后再点击')
        if not linkphone.isdigit():
            return HttpResponse('手机号输入有误')
        # 存数据库
        idc = IDC()
        try:
            idc.name = name
            idc.linkman = linkman
            idc.linkphone = linkphone
            idc.network_segment = network
            idc.address = address
            idc.operator = operator
            idc.type = idc_type
            idc.bandwidth = band
            idc.save()
            ip = request.META.get('REMOTE_HOST')
            msg = "创建IDC :%s" % idc.name
            save_log.delay(request.user.realname, action='add', resource='IDC机房表', operating=msg, ip=ip)
        except django.db.utils.IntegrityError as e:
            print(e)
            return HttpResponse('用户名重复请重新输入')
        return HttpResponse('ok')

def get_idc(request, id):
    asset = IDC.objects.filter(id=id).values('name', 'linkman', 'linkphone', 'address', 'network_segment', 'bandwidth',
                                             'operator', 'type')
    data = json.dumps(list(asset))
    return HttpResponse(data)


def update_idc(request, id):
    idc = IDC.get_by_id(id)
    idc.name = request.GET.get('name')
    idc.linkphone = request.GET.get('linkphone')
    idc.linkman = request.GET.get('linkman')
    idc.bandwidth = request.GET.get('bandwidth')
    idc.network_segment = request.GET.get('network_segment')
    idc.address = request.GET.get('address')
    idc.type = request.GET.get('type')
    idc.operator = request.GET.get('operator')
    try:
        idc.save()
        ip = request.META.get('REMOTE_HOST')
        msg = "修改IDC: %s" % idc.name
        save_log.delay(request.user.realname, action='change', resource='IDC机房表', operating=msg, ip=ip)
    except django.db.utils.IntegrityError:
        return HttpResponse('no')
    return HttpResponse('ok')
