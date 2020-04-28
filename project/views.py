import json
from django.shortcuts import render, reverse, HttpResponseRedirect
from django.views.generic import CreateView, View, UpdateView
from django.urls import reverse_lazy
from django.http import JsonResponse
from django_filters.views import FilterView
from .models import Project
# from ..tasks import save_log
from .filters import ProjectFilter
from .forms import CreateProjectForm, UpdateProjectForm
from django.db.models import Q


class ProjectView(FilterView):
    model = Project
    template_name = 'project/project.html'
    filterset_class = ProjectFilter

    def get_queryset(self):
        # 如果时超级管理员则返回所有的项目
        user = self.request.user
        if user.is_superuser:
            return Project.get_all().select_related("creator").prefetch_related("auth_users")
        else:
            return Project.objects.filter(Q(auth_users=user) | Q(creator=user)).prefetch_related(
                "auth_users").select_related("creator")


class CreateProjectView(CreateView):
    template_name = 'project/create_project.html'
    context_object_name = 'form'
    # 需要使用懒加载
    success_url = reverse_lazy('project')
    form_class = CreateProjectForm

    def form_valid(self, form):
        p = form.save(commit=False)
        p.creator = self.request.user
        p.save()
        form.save_m2m()

        # 从post请求中获得选择的用户，然后使用 set方法
        p.assets_set.set(form.cleaned_data.get("assets_set", []))

        ip = self.request.META.get('REMOTE_HOST')
        msg = "创建项目: %s" % form.cleaned_data['project_name']
        # save_log.delay(self.request.user.realname, action='add', resource='项目表', operating=msg, ip=ip)
        return HttpResponseRedirect(reverse('project'))

    def form_invalid(self, form):
        return render(self.request, self.template_name, {"form": form})


class UpdateProjectView(UpdateView):
    template_name = 'project/update_project.html'
    model = Project
    context_object_name = "form"
    pk_url_kwarg = "id"

    def get_form(self, form_class=None):
        assets_list = self.get_object().assets_set.all()
        kwargs = self.get_form_kwargs()
        kwargs.update({"initial": {"assets_set": assets_list}})
        return UpdateProjectForm(**kwargs)

    def form_valid(self, form):
        form.save()
        self.get_object().assets_set.set(form.cleaned_data.get("assets_set", []))
        ip = self.request.META.get('REMOTE_HOST')
        msg = "修改项目: %s" % form.cleaned_data['project_name']
        # save_log.delay(self.request.user.realname, action='change', resource='项目表', operating=msg, ip=ip)
        return HttpResponseRedirect(reverse('project'))

    def form_invalid(self, form):
        return render(self.request, self.template_name, {"form": form})
