import os
from django.shortcuts import render, HttpResponseRedirect, reverse, Http404
from django.contrib.auth.decorators import permission_required
from django.views.generic import View, ListView, DetailView, UpdateView
from django.utils.decorators import method_decorator
from django.http import JsonResponse, QueryDict
from django_filters.views import FilterView
from assets.models import Assets
from ttcmdb.settings import BASE_DIR
from ..models import AnsiblePlaybook, AnsiblePlaybookLog
from ..forms import CreatePlaybook
from ..filters import PlaybookLogFilter


class CreatePlaybookView(View):
    """
    创建playbook类
    """
    template_name = "task/playbook/create_playbook.html"

    def get(self, request, **kwargs):
        """
        返回页面和 表单
        :param request:
        :param kwargs:
        :return:
        """
        form = CreatePlaybook()
        return render(request, self.template_name, locals())

    def post(self, request, **kwargs):
        # 获取上传的文件，如果，有则从文件读取，没有从content读取 vb
        form = CreatePlaybook(request.POST)
        content = form.data.get("playbook_content")
        file = request.FILES.get("playbook_file")
        if file:
            dir = os.path.join(BASE_DIR, 'static', 'playbooks', file.name)
            with open(dir, "wb") as f:
                for i in file.chunks():
                    f.write(i)
                f.close()

        if form.is_valid():
            pb = form.save(commit=False)
            pb.playbook_user = request.user

            # 如果有上传文件，则读取文件,如果没有直接存库
            if file:
                content = ""
                with open(dir, 'r') as f:
                    for line in f.readlines():
                        content += line
                f.close()
                pb.playbook_content = content
                pb.save()
            elif content:
                # 没有上传直接存库
                pb = form.save(commit=False)
                pb.playbook_user = request.user
                pb.save()
            else:
                # 什么都没有报错返回
                return render(request, self.template_name, {"form": form, "error": "必须填写一处"})
        else:
            return render(request, self.template_name, {"form": form})
        return HttpResponseRedirect(reverse("playbooks"))


class PlayBooksView(ListView):
    """
    展示playbook 的所有

    """
    template_name = "task/playbook/playbooks.html"
    context_object_name = "pbs"

    def get_queryset(self):
        return AnsiblePlaybook.objects.all().select_related("playbook_user")

    def delete(self, request, **kwargs):
        ret = {'code': 200, 'msg': None}
        body = QueryDict(request.body)
        id = body.get('id')
        print(id)
        try:
            pb = AnsiblePlaybook.objects.get(id=id)
            pb.delete()
        except AnsiblePlaybook.DoesNotExist:
            ret["msg"] = "没有这个数据"
            ret["code"] = 400
            return JsonResponse(ret)
        # 异步执行删除
        return JsonResponse(ret)


class PlayBookInfoView(UpdateView):
    """
        playbook详情
    """
    template_name = "task/playbook/playbook_info.html"
    model = AnsiblePlaybook
    form_class = CreatePlaybook
    context_object_name = "form"
    pk_url_kwarg = "pk"

    def form_valid(self, form):
        pb = form.save(commit=False)
        content = form.data.get("playbook_content")
        file = self.request.FILES.get("playbook_file")
        if file:
            dir = os.path.join(BASE_DIR, 'static', 'playbooks', file.name)
            with open(dir, "wb") as f:
                for i in file.chunks():
                    f.write(i)
                f.close()
            content = ""
            with open(dir, 'r') as f:
                for line in f.readlines():
                    content += line
                f.close()
            pb.playbook_content = content
            pb.save()
        elif content:
            pb.save()
        else:
            # 什么都没有报错返回
            return render(self.request, self.template_name, {"form": form, "error": "上传剧本或在线编写必须填选一处"})

        return HttpResponseRedirect(reverse("playbooks"))


class RunPlaybookView(View):
    """
    执行playbook的接口
    """
    template_name = "task/playbook/run_playbook.html"

    def get(self, request, **kwargs):
        pbl = AnsiblePlaybook.objects.only("id", "playbook_name").all()
        return render(request, self.template_name, locals())


class PlayBookLogListView(FilterView):
    model = AnsiblePlaybookLog
    template_name = "task/playbook/playbook_log_list.html"
    filterset_class = PlaybookLogFilter


class PlayBookDetailView(DetailView):
    template_name = "task/playbook/playbook_log.html"
    model = AnsiblePlaybookLog
    context_object_name = "module"
    pk_url_kwarg = "id"

    def get_context_data(self, **kwargs):
        id = self.kwargs.get("id")
        # 查询出该pblog
        pbl = AnsiblePlaybookLog.objects.only("playbook_result").get(id=id)
        context = super(PlayBookDetailView, self).get_context_data(**kwargs)

        _ = ""
        for __ in eval(pbl.playbook_result):
            _ += __
        context.update({"result": _})
        return context
