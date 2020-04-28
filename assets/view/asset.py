# ~*~ coding: utf-8 ~*~
import re
from django.db.models import Q
from django.urls import reverse_lazy
from django.shortcuts import HttpResponseRedirect, reverse, render, Http404, get_object_or_404
from django.views.generic import DetailView, ListView, CreateView, UpdateView
from project.models import Project
from ..forms import AssetForm
# from logger.tasks import save_log
from ..models import Assets


def ymd(date):
    try:
        date = re.findall('(\d+)/(\d+)/(\d+)', str(date))[0]
        y = date[0]
        m = date[1]
        d = date[2]
    except IndexError:
        return None
    return y + '-' + m + '-' + d


class AssetsList(ListView):
    template_name = 'assets/asset/assets_list.html'
    context_object_name = "assets_list"
    paginate_by = 20

    def get(self, request, *args, **kwargs):
        ip = request.GET.get("ip", None)
        if ip:
            # 得到当前用户能看到的
            queryset = self.get_queryset().filter(ip__contains=ip)
            return render(request, "assets/asset/assets_list.html", {"assets_list": queryset})
        else:
            return super().get(request, *args, **kwargs)

    def get_queryset(self):
        project_name = self.request.GET.get('project', None)
        # ip = self.request.GET.get("ip", None)
        # 必须是超管才能看所有，不是超管只能看到自己的项目下的资产
        user = self.request.user
        # 是否有项目
        if project_name:
            queryset = self.filter_by_project(user, project_name)
        else:
            # 返回所有
            queryset = self.filter_all(user)
        # 然后判断ip筛选

        ordering = self.get_ordering()
        if ordering:
            if isinstance(ordering, str):
                ordering = (ordering,)
            queryset = queryset.order_by(*ordering)

        return queryset

    # 查询项目资产
    def filter_by_project(self, user, project_name):
        """ 超级用户优先所有 """
        if user.is_superuser:
            project_obj = get_object_or_404(Project, project_name=project_name)
            return Assets.objects.only(
                'id', 'asset_type', 'ip', 'is_pass', 'status', "cpu", "ram", "disk"
            ).filter(project=project_obj)
        else:
            projects = Project.objects.filter(project_name=project_name).filter(
                Q(auth_users=user) | Q(creator=user)).prefetch_related(
                "auth_users").select_related("creator")
            queryset = Assets.objects.none()
            for p in projects:
                assets = Assets.objects.only('id', 'asset_type', 'ip', 'is_pass', 'status', 'cpu', 'ram', 'disk'
                                             ).filter(project=p)
                # 做按位与
                # 注意这里采用的方式。如果 Model相同，而且没有用切片，并且字段一样时可以这样用
                queryset = queryset | assets
            return queryset

    # ip 的模糊匹配
    def filter_by_ip(self, user, ip, queryset=None):
        if user.is_superuser:
            queryset = Assets.objects.only('id', 'asset_type', 'ip', 'is_pass', 'status', 'cpu', 'ram', 'disk'
                                           ).filter(ip__contains=ip)
            return queryset
        else:
            return queryset.filter(ip__contains=ip)

    def filter_all(self, user):
        if user.is_superuser:
            return Assets.objects.only('id', 'asset_type', 'ip', 'is_pass', 'status', 'cpu', 'ram', 'disk').all()
        else:
            # 先要遍历
            projects = Project.objects.filter(Q(auth_users=user) | Q(creator=user)).prefetch_related(
                "auth_users").select_related("creator")
            # 得到包含此用户的所有项目
            queryset = Assets.objects.none()
            for project in projects:
                assets = Assets.objects.only('id', 'asset_type', 'ip', 'is_pass', 'status', 'cpu', 'ram', 'disk'
                                             ).filter(project=project)
                queryset = queryset | assets
            return queryset


class AssetInfo(DetailView):
    template_name = 'assets/asset/assets_info.html'
    context_object_name = 'asset'
    pk_url_kwarg = 'id'

    def get_queryset(self):
        return Assets.objects.all().prefetch_related("tags", "system_users").select_related("project", "idc")


class CreateAssetView(CreateView):
    model = Assets
    template_name = "assets/asset/assets_create.html"
    context_object_name = "form"
    form_class = AssetForm

    def form_valid(self, form):
        asset = form.save(commit=False)
        asset.creator = self.request.user
        asset.save()
        form.save_m2m()

        ip = self.request.META.get('REMOTE_HOST')
        msg = "创建资产信息:%s" % form.cleaned_data["ip"]
        # save_log.delay(self.request.user.realname, action='add', resource='Assets资产表', operating=msg, ip=ip)
        return HttpResponseRedirect(reverse("assets-list"))


class UpdateAssetView(UpdateView):
    template_name = 'assets/asset/asset_update.html'
    pk_url_kwarg = "id"
    model = Assets
    form_class = AssetForm
    context_object_name = "form"
    success_url = reverse_lazy("assets-list")

    def form_valid(self, form):
        form.save()
        # 存入操作日志
        ip = self.request.META.get('REMOTE_HOST')
        msg = "修改: %s的资产信息" % form.cleaned_data["ip"]
        # save_log.delay(self.request.user.realname, action='change', resource='Assets资产表', operating=msg, ip=ip)

        return HttpResponseRedirect(reverse('assets-list'))


def asset_active_update(request, id):
    if request.method == 'GET':
        asset = Assets.get_by_id(id)
        if asset is None:
            raise Http404
        if asset.is_active:
            asset.is_active = False
        else:
            asset.is_active = True
        id = asset.id
        asset.save(force_update=True)
        # 存入日志
        ip = request.META.get('REMOTE_HOST')
        msg = '修改 %s 资产的激活状态' % asset.ip
        # save_log.delay(request.user.realname, action='change', resource='Assets资产表', operating=msg, ip=ip)
        url = '/assets/info/' + str(id)
        return HttpResponseRedirect(url)
