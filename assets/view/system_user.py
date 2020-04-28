from django.shortcuts import HttpResponseRedirect, reverse, render
from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy
from django_filters.views import FilterView
from ..filters import PushUserFilter
from ..models import SystemUser, PushSystemUserLog
from ..forms import CreateSystemUserForm, UpdateSystemUserForm


# from logger.tasks import save_log

class SystemUserList(ListView):
    template_name = 'assets/server_push_user/server_user.html'
    context_object_name = 'system_users'
    model = SystemUser
    page_kwarg = 20
    ordering = "-create_time"


class CreateSystemUserView(CreateView):
    template_name = 'assets/server_push_user/create_server_user.html'
    context_object_name = 'form'
    form_class = CreateSystemUserForm

    def form_valid(self, form):
        su = form.save(commit=False)
        su.creator = self.request.user
        su.save()
        ip = self.request.META.get('REMOTE_HOST')
        msg = "创建系统用户:" + su.username
        # save_log.delay(self.request.user.realname, action='add', resource='系统用户表', operating=msg, ip=ip)
        return HttpResponseRedirect(reverse('assets-system-user'))

    def form_invalid(self, form):
        return render(self.request, 'assets/server_push_user/create_server_user.html', {"form": form})


class UpdateSystemUserView(UpdateView):
    template_name = 'assets/server_push_user/update_server_user.html'
    model = SystemUser
    form_class = UpdateSystemUserForm
    context_object_name = 'form'
    pk_url_kwarg = 'id'
    success_url = reverse_lazy('assets-system-user')


class PushUserLogView(FilterView):
    template_name = 'assets/server_push_user/push_user.html'
    page_kwarg = 100
    filterset_class = PushUserFilter

    def get_queryset(self):
        id = self.request.GET.get('set', None)
        if not id:
            queryset = PushSystemUserLog.objects.all().select_related('pusher')
            return queryset
        else:
            su = SystemUser.get_by_id(id)
            queryset = PushSystemUserLog.objects.filter(username=su.username).select_related('pusher')
            return queryset
