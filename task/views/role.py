import json, os, shutil
from django.shortcuts import render, HttpResponseRedirect, HttpResponse, reverse, Http404
from django.views.generic import View, ListView, DetailView
from django.http import JsonResponse, QueryDict
from django.views.decorators.csrf import csrf_exempt
from assets.models import Assets
from ttcmdb.settings import ANSIBLE_ROLE_PATH, BASE_DIR
from django_filters.views import FilterView
from ..filters import RoleLogFilter
from ..models import RunRoleLog, RunRoleScript, AnsibleRole


class RoleListView(ListView):
    """
    显示所有role
    """
    template_name = "task/role/role_list.html"
    context_object_name = "role_list"

    def get_queryset(self):
        return AnsibleRole.objects.select_related("role_user").all()

    def delete(self, request, **kwargs):
        """
        删除role
        :param request:
        :param kwargs:
        :return:
        """
        ret = {'code': 200, 'error': None, }
        body = QueryDict(request.body)
        id = body.get('id')
        role = AnsibleRole.objects.filter(id=id).first()

        if not role:
            raise Http404
        # 删除文件
        try:
            path = str(role.role_file)
            shutil.rmtree(path)
        except Exception as e:
            print(e)
        finally:
            role.delete()

        return JsonResponse(ret)


class RoleAddView(View):
    """
    显示所有role
    """
    template_name = "task/role/role_add.html"

    def get(self, request, **kwargs):
        """
        从role-list提交后发送到post请求，然后存库等操作，
        存入数据库后生成文件，生成完 使用reverse到get请求，
        get携带钢创建的role的id 再通过id 查询出所需要参数
        :param request:
        :param kwargs:
        :return: 返回在线编辑页面
        """
        if "roid" in request.GET:
            rid = request.GET.get("roid")
            role = AnsibleRole.objects.select_related("role_user").get(id=rid)
            context = {
                "role_name": role.role_name,
                "root_path": ANSIBLE_ROLE_PATH
            }
            return render(request, self.template_name, context)
        raise Http404

    def post(self, request, **kwargs):
        """
        获取传递的post参数，然后存库，
        存库成功后，创建一个role名的文件夹，再依次创建固定格式内容
        :param request:
        :param kwargs:
        :return:
        """
        # 存库
        role_name = request.POST.get('role_name', None)
        role_desc = request.POST.get('role_desc', None)
        if not role_name:
            raise Http404
        root_path = ANSIBLE_ROLE_PATH
        try:
            role = AnsibleRole.objects.select_related('role_user').create(
                role_name=role_name,
                role_file='{}/{}'.format(root_path, role_name),
                role_user=request.user,
                role_desc=role_desc
            )
        except Exception as e:
            return render(request, 'other/400.html', {"error": "错误:Role命名重复，请更换Role名再试! ", "desc": str(e)})

        # 存储文件`
        # 先拼接出要复制的模板
        default = os.path.join(ANSIBLE_ROLE_PATH, "defaultRoletemplate")
        # 然后加上存入到数据库的role名
        aims = os.path.join(ANSIBLE_ROLE_PATH, role_name)
        # 拷贝到模板目录下
        shutil.copytree(default, aims)
        # 返回get请求
        url = reverse("role") + "?roid=" + str(role.id)
        return HttpResponseRedirect(url)


# #需要写连个视图 一个处理节点，一个处理文件
class NodesView(View):
    ret = {"code": 200, "error": None}
    """
    处理节点的  创建删除，修改功能
    """

    def get(self, request, **kwargs):
        ret = {"code": 200, "error": None, "content": None}
        path = request.GET.get('p_name', None)
        name = request.GET.get('name', None)
        if path and name:
            try:
                path = os.path.join(path, name)
                with open(path, 'rb') as f:
                    content = f.read()
                    f.close()
                # 得到全部
                try:
                    ret["content"] = content.decode('utf-8')
                except UnicodeDecodeError:
                    ret["content"] = content.decode("gb2312", "ignore")
            except FileNotFoundError:
                ret["code"] = 400
                ret["error"] = "没有这个文件 %s" % name
        return JsonResponse(ret)

    def post(self, request, **kwargs):
        ret = {"code": 200, "error": None}
        """
        用于更新节点名称
        """

        path = request.POST.get('p_name', None)
        name = request.POST.get('name', None)
        new_name = request.POST.get('new_name', None)
        is_Parent = request.POST.get('isParent', None)
        # 判断这几个参数有无
        # 然后根据路径取查询该文件/文件夹然后改名
        if path and name and new_name and is_Parent:
            # 先判断是不是新建文件，
            if name[0:8] == "new node":
                # 是新建节点
                if is_Parent == 'true':
                    # 是文件夹
                    dir = os.path.join(path, new_name)
                    os.mkdir(dir)
                else:
                    # 是文件
                    dir = os.path.join(path, new_name)
                    os.mknod(dir)
            else:
                try:
                    # 重命名文件
                    old = os.path.join(path, name)
                    new = os.path.join(path, new_name)
                    os.rename(old, new)
                except FileNotFoundError:
                    ret["code"] = 400
                    ret["error"] = "文件不存在 !"
                    return JsonResponse(ret)

        else:
            raise Http404
        return JsonResponse(ret)

    def delete(self, request, **kwargs):
        body = QueryDict(request.body)
        path = body.get('p_name', None)
        name = body.get('name', None)
        is_Parent = body.get('isParent', None)

        if name and path and is_Parent:
            if is_Parent == 'true':
                # 是文件夹
                path = os.path.join(path, name)
                shutil.rmtree(path)
            else:
                # 是文件
                path = os.path.join(path, name)
                os.remove(path)
        return JsonResponse(self.ret)

    def put(self, request, **kwargs):
        ret = {"code": 200, "error": None}
        body = QueryDict(request.body)
        path = body.get('p_name', None)
        name = body.get('name', None)
        content = body.get('content', None)
        if name and path:
            try:
                path = os.path.join(path, name)
                with open(path, 'w+') as f:
                    f.write(content)
                    f.close()
            except Exception as e:
                ret["code"] = 400
                ret["error"] = "出错:" + str(e)

        return JsonResponse(ret)


def upload_file(request):
    """
    节点上传文件
    :param request:
    :return:
    """
    ret = {"code": 200, "error": None, "f_name": None}
    if request.method == 'POST':
        # 如果是post请求，就取出文件
        path = request.POST.get('p_name', None)
        name = request.POST.get('name', None)
        file = request.FILES.get("file", None)
        if path and name and file:
            # 取出文件，然后存到指定位置
            f_name = file.name
            dirs = os.path.join(path, name, f_name)
            with open(dirs, "wb") as f:
                for i in file.chunks():
                    f.write(i)
                f.close()
            ret["f_name"] = f_name
            return JsonResponse(ret)
    raise Http404


class RoleEditView(View):
    """
    显示所有role
    """
    template_name = "task/role/role_edit.html"

    def get(self, request, **kwargs):
        """
        通过id 取值
        :return: 返回在线编辑页面
        """
        rid = self.kwargs.get("id", None)
        if not rid:
            raise Http404
        role = AnsibleRole.objects.select_related("role_user").get(id=rid)
        context = {
            "role_name": role.role_name,
            "root_path": ANSIBLE_ROLE_PATH,
            "id": role.id
        }
        return render(request, self.template_name, context)


class RunRoleView(View):
    template_name = "task/role/run_role.html"

    def get(self, request, **kwargs):
        scripts = RunRoleScript.objects.only("id", "r_name", "r_content", "chang_time").all().values()

        context = {
            "s_l": Assets.objects.only("id", "ip").all(),
            "role_script": scripts,
            "script": scripts[:5]
        }
        return render(request, self.template_name, context)


class RoleScriptListVIew(View):
    template_name = "task/role/role_script_list.html"

    def get(self, request, **kwargs):
        # 返回所有的数据
        sl = RunRoleScript.objects.select_related("creator").all().values()
        context = {
            "role_script_list": sl,
            "roles": AnsibleRole.objects.only("id", "role_name").all()
        }
        return render(request, self.template_name, context)

    def post(self, request, **kwargs):
        script_name = request.POST.get("role_name", None)
        roles = request.POST.getlist("roles", None)

        # 通过roles 生成脚本
        content = """
---
- hosts: default
  gather_facts: false
  roles:
"""

        for rid in roles:
            # 遍历id
            id = int(rid)
            role = AnsibleRole.get_name_by_id(id)
            if role:
                content += "    - { role: %s,        tags: %s }\n" % (role.role_name, role.role_name)
        # 存储到数据克
        role_script = RunRoleScript(r_name=script_name, r_content=content, creator=request.user)
        role_script.save()

        return HttpResponseRedirect(reverse("role-script"))

    def delete(self, request, **kwargs):
        ret = {'status': True, 'error': None, }
        body = QueryDict(request.body)
        id = body.get('id')

        rs = RunRoleScript.get_by_id(id)
        if not rs:
            raise Http404
        rs.delete()
        return JsonResponse(ret)


class DetailRoleScript(View):
    template_name = "task/role/change-script.html"

    def get(self, request, **kwargs):
        id = request.GET.get("id", None)
        if id:
            return render(request, self.template_name, {"id": id})
        raise Http404

    def post(self, request, **kwargs):
        """返回json字符串"""
        id = request.POST.get("id", None)
        role_script = RunRoleScript.get_by_id(id)
        if role_script:
            result = {
                "code": 200,
                "name": role_script.r_name,
                "content": role_script.r_content
            }
        else:
            result = {"code": 400, "error": "错误的参数，获取失败"}
        return JsonResponse(result)

    def put(self, request, **kwargs):
        """修改 通过name得到，然后覆盖"""
        body = QueryDict(request.body)
        name = body.get("name", None)
        if name:
            rs = RunRoleScript.get_by_name(name)
            if rs:
                rs.r_content = body.get("content", None)
                # 保存
                rs.save()
                return JsonResponse({"code": 200})
            return JsonResponse({"code": 400, "error": "无效的name"})
        raise Http404


@csrf_exempt
def ge_detail(request, id=None):
    name = request.POST.get('name')
    p_name = request.POST.get('p_name')
    if name and p_name:
        nodes = []
        # 建立节点
        path_names = os.listdir(os.path.join(p_name, name))
        # 获取目标路径下的所有文件
        path_names.sort()

        for path_name in path_names:

            node = {'name': path_name, 'p_name': p_name + '/' + name}
            if os.path.isdir(os.path.join(p_name, name, path_name)):
                node['isParent'] = True
            else:
                node['isParent'] = False
            nodes.append(node)
        return HttpResponse(json.dumps(nodes))
    else:
        role_name = AnsibleRole.objects.get(id=id).role_name
        node = {'name': role_name, 'isParent': True, 'p_name': ANSIBLE_ROLE_PATH}
        return HttpResponse(json.dumps(node))


def upload_role(request):
    if request.method == 'POST':
        # 如果是post请求，就取出文件
        desc = request.POST.get('role_desc', None)
        file = request.FILES.get("role_file", None)

        if file:
            # 取出文件，然后存到指定位置
            f_name = file.name
            name = f_name[:-4]
            dirs = os.path.join(BASE_DIR, 'static', 'roles', f_name)

            with open(dirs, "wb") as f:
                for i in file.chunks():
                    f.write(i)
                f.close()
            # 存储完成后 ，解压该文件
            # 判断文件名是那种压缩包
            extract = ANSIBLE_ROLE_PATH

            if f_name.endswith(".zip"):
                # 导入zipfile
                zip = __import__("zipfile")
                z = zip.ZipFile(dirs, 'r')
                # 解压到role目录
                z.extractall(extract)
                z.close()

            elif f_name.endswith(".tar"):

                tar = __import__("tarfile")
                t = tar.open(dirs, 'r')
                t.extractall(extract)
                t.close()
            else:
                # 都不是这两种  删除
                os.remove(dirs)
                return render(request, 'other/400.html', {"error": "上传了非 zip/tar 类型的文件", "desc": "请重新上传或查看帮助"})

            # 存库
            try:
                AnsibleRole.objects.select_related('role_user').create(
                    role_name=name,
                    role_file='{}/{}'.format(ANSIBLE_ROLE_PATH, name),
                    role_user=request.user,
                    role_desc=desc
                )
            except Exception as e:
                # 报错后删除
                os.remove(dirs)
                shutil.rmtree('{}/{}'.format(ANSIBLE_ROLE_PATH, name))
                return render(request, 'other/400.html', {"error": "不可预期的错误:", "desc": str(e)})
        return HttpResponseRedirect(reverse("roles"))
    raise Http404


class RoleLogListView(FilterView):
    model = RunRoleLog
    template_name = "task/role/role_log_list.html"
    filterset_class = RoleLogFilter


class RoleLogView(DetailView):
    template_name = "task/role/role_log.html"
    model = RunRoleLog
    context_object_name = "module"
    pk_url_kwarg = "id"

    def get_context_data(self, **kwargs):
        id = self.kwargs.get("id")
        # 查询出该role_id
        rl = RunRoleLog.objects.only("role_result").get(id=id)
        context = super(RoleLogView, self).get_context_data(**kwargs)

        _ = ""
        for __ in eval(rl.role_result):
            _ += __
        context.update({"result": _})
        return context
