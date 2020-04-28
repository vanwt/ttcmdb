from django.shortcuts import render, HttpResponse, HttpResponseRedirect, reverse, get_object_or_404, Http404
from django.views.generic import View, DetailView, ListView, UpdateView
# 导入django自带的加密模块
from django.contrib.auth.hashers import make_password
from .models import User, Menu, UrlPermission, Role
from datetime import datetime
from django.urls import reverse_lazy
from django.contrib.auth import login, logout
from django.http import JsonResponse
from .forms import *
import requests


# Create your views here.


# 用户登录
class LoginView(View):
    template_name = 'user/login.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        # 接受forms传参
        account = request.POST.get("account", None)
        password = request.POST.get("password", None)

        if account and password:
            # 判断
            user = User.check_user_password(account, password)
            if user:
                login(request, user=user)
                # 存储日志
                ip = request.META.get('REMOTE_HOST', None)
                # save_login_log.delay(user.realname, ip=ip, status=1)
                return HttpResponseRedirect(reverse('index'))
            else:
                # save_login_log.delay(account, ip=request.META.get('REMOTE_HOST', None), status=0)
                return render(request, self.template_name, {"msg": "账户或密码有误"})
        return render(request, self.template_name, {"msg": "登录失败"})


def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))


class UserInfo(DetailView):
    template_name = 'user/userinfo.html'
    context_object_name = 'user'

    def get_object(self, queryset=None):
        return self.request.user


class UserList(ListView):
    template_name = 'user/user_list.html'
    queryset = User.get_all()
    paginate_by = 10
    context_object_name = 'users_list'
    # 按id排序
    ordering = ['id']


class UserCreate(View):
    template_name = 'user/create_user.html'

    def get(self, request, *args, **kwargs):
        form = CreateUserForm()

        return render(request, self.template_name, {"form": form, "login_user": request.user})

    def post(self, request, *args, **kwargs):
        user = request.user
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # 对密码加密
            pwd = form.cleaned_data['password']
            user.password = make_password(pwd, None, 'pbkdf2_sha256')
            user.is_active = True
            user.create_time = datetime.now()
            user.save()
            form.save_m2m()
            ip = request.META.get('REMOTE_HOST')
            msg = "创建用户: %s" % user.username
            # save_log.delay(request.user.realname, action='add', resource='用户表', operating=msg, ip=ip)
            return HttpResponseRedirect(reverse('user-list'))
        return render(request, self.template_name, {"form": form, "login_user": user})


class RegisterView(View):
    """逻辑是 钉钉扫码后注册信息，然后登录,然后设置用户名 or 密码"""

    def get(self, request, **kwargs):
        return render(request, 'user/dd_register.html')


# 修改用户
class UpdateUserView(UpdateView):
    template_name = 'user/user_update.html'
    context_object_name = 'form'
    model = User
    form_class = UpdateUserForm
    pk_url_kwarg = 'id'

    def form_valid(self, form):
        # 判断files 有没有文件，有文件就存储到users-img
        # 如果存在，就要先暂时不保存，

        form.save()

        # 判断是不是超级用户,如果是超级用户就需要返回用户列表，否则返回info
        next = self.request.GET.get("next", None)
        if next:
            return HttpResponseRedirect(next)
        else:
            if self.request.user.is_superuser:
                return HttpResponseRedirect(reverse("user-list"))
            else:
                return HttpResponseRedirect("/user/info/" + str(id) + '/')


# 修改密码
class UpdatePassword(View):
    template_name = 'user/update_pwd.html'

    def get(self, request, *args, **kwargs):
        # 如果修改的不是自身
        form = UpdatePasswordForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        id = self.kwargs.get('id')
        if id != str(request.user.id):
            return render(request, "other/403.html")

        form = UpdatePasswordForm(request.POST)
        if form.is_valid():
            user = User.get_by_id(id)
            # 如果是新用户可以直接设置密码
            if user.password:
                # 判断旧密码是否正确
                if not user.check_password(form.cleaned_data['old_password']):
                    return render(request, self.template_name, {"form": form, "old_msg": "旧密码错误"})

            # 判断两次是否输入一直
            if form.cleaned_data['new_password'] != form.cleaned_data['new_pwd']:
                return render(request, self.template_name,
                              {"form": form, "pwd_msg": "两次密码输入不一致"})

            # 验证通过则存储新密码 并加密sha256
            pwd = form.cleaned_data['new_password']
            user.set_password(pwd)
            user.save()
            # 让用户重新登录
            if user.is_superuser:
                return HttpResponseRedirect(reverse_lazy('user-list'))
            return HttpResponseRedirect('/user/info/' + str(user.id) + "/")

        context = {
            "form": form, "id": id
        }

        return render(request, self.template_name, context)


class MenuListView(ListView):
    model = Menu
    template_name = "user/menu_list.html"
    context_object_name = "menu_list"


class UrlPermissionView(ListView):
    model = UrlPermission
    template_name = "user/urlpermission.html"
    context_object_name = "url_list"


class RoleView(ListView):
    model = Role
    template_name = "user/role.html"
    context_object_name = "role_list"


# 删除用户
def user_delete(request, id):
    ret = {'code': 200, 'error': None}
    from django.db import IntegrityError
    try:
        user = get_object_or_404(User, id=id)
        user.delete()
    except IntegrityError as e:
        ret["error"] = "请删除或修改与此用户相关联的所有操作后再次尝试"
        return JsonResponse(ret)
    return JsonResponse(ret)
