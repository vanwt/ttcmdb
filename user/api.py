from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from .models import User, Menu, UrlPermission, Role
from .serializers import MenuSerializers, UrlPermissionSerializers, RoleSerializers


class MenuViewSet(ModelViewSet):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializers


class UrlPermissionViewSet(ModelViewSet):
    queryset = UrlPermission.objects.all()
    serializer_class = UrlPermissionSerializers


class RoleViewSet(ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializers


class RestPasswordApiView(APIView):
    def get(self, request, **kwargs):
        result = {"errcode": 0, "msg": None}
        id = self.kwargs.get("id", None)
        try:
            user = User.get_by_id(id)
            user.set_password('123456')
            user.save()
        except AttributeError:
            result["errcode"] = 1
            result["msg"] = "修改密码失败"
            return Response(result)
        return Response(result)


class ChangMenuStatusApiView(APIView):
    def get(self, request, **kwargs):
        result = {"errcode": 0, "msg": None}
        id = self.kwargs.get("id", None)
        menu = Menu.objects.filter(id=id).first()
        if menu:
            if menu.status:
                menu.status = False
                menu.save()
            else:
                menu.status = True
                menu.save()
            return Response(result)

        result["errcode"] = 1
        result["msg"] = "不存在的对象"
        return Response(result)


class ChangeUrlPermissionStatus(APIView):
    def get(self, request, **kwargs):
        result = {"errcode": 0, "msg": None}
        id = self.kwargs.get("id", None)
        up = UrlPermission.objects.filter(id=id).first()
        if up:
            if up.status:
                up.status = False
                up.save()
            else:
                up.status = True
                up.save()
            return Response(result)

        result["errcode"] = 1
        result["msg"] = "不存在的对象"
        return Response(result)


class ChangeRoleStatus(APIView):
    def get(self, request, **kwargs):
        result = {"errcode": 0, "msg": None}
        id = self.kwargs.get("id", None)
        up = Role.objects.filter(id=id).first()
        if up:
            if up.status:
                up.status = False
                up.save()
            else:
                up.status = True
                up.save()
            return Response(result)

        result["errcode"] = 1
        result["msg"] = "不存在的对象"
        return Response(result)


class GetRoleAllUser(APIView):
    def get(self, request, **kwargs):
        """ 获取当前角色的所属用户 """
        result = {"errcode": 0, "msg": None}
        id = request.GET.get("id", None)
        queryset = User.objects.only("id", "realname").all()
        role = Role.objects.filter(id=id).first()
        u_list = []
        if role:
            role_users = role.users.only("id").all()
            role_ids = [ru.id for ru in role_users]

            for au in queryset:
                r = {}
                r["id"] = au.id
                r["realname"] = au.realname
                if au.id in role_ids:
                    r["selected"] = True
                else:
                    r["selected"] = False
                u_list.append(r)
            result["msg"] = u_list
        else:
            result = {"errcode": 1, "msg": "错误的参数"}
        return Response(result)

    def post(self, request, **kwargs):
        """ 修改 角色的用户信息 """
        result = {"errcode": 0, "msg": None}
        id = request.POST.get("id", None)
        user_ids = request.POST.getlist("users[]", [])
        role = Role.objects.filter(id=id).first()
        if role:
            role.users.set(user_ids)
            role.save()
            return Response(result)
        result["errcode"] = 1
        result["msg"] = "参数错误"
        return Response(result)


class GetRoleAllPermission(APIView):
    def get(self, request, **kwargs):
        """ 获取当前角色的所有权限 """
        result = {"errcode": 0, "msg": None}
        id = request.GET.get("id", None)
        queryset = UrlPermission.objects.only("id", "title").all()
        role = Role.objects.filter(id=id).first()
        per_list = []
        if role:
            role_permissions = role.permission.only("id", "title").all()
            per_ids = [ru.id for ru in role_permissions]

            for per in queryset:
                r = {}
                r["id"] = per.id
                r["title"] = "%s :%s" % (per.title, per.method)
                if per.id in per_ids:
                    r["selected"] = True
                else:
                    r["selected"] = False
                per_list.append(r)
            result["msg"] = per_list
        else:
            result = {"errcode": 1, "msg": "错误的参数"}
        return Response(result)

    def post(self, request, **kwargs):
        """ 修改 角色的用户信息 """
        result = {"errcode": 0, "msg": None}
        id = request.POST.get("id", None)
        per_ids = request.POST.getlist("permissions[]", [])
        role = Role.objects.filter(id=id).first()
        if role:
            role.permission.set(per_ids)
            role.save()
            return Response(result)
        result["errcode"] = 1
        result["msg"] = "参数错误"
        return Response(result)


class GetRoleAllMenu(APIView):
    def get(self, request, **kwargs):
        """ 获取当前角色的所有权限 """
        result = {"errcode": 0, "msg": None}
        id = request.GET.get("id", None)
        queryset = Menu.objects.only("id", "title").all()
        role = Role.objects.filter(id=id).first()
        per_list = []
        if role:
            role_menus = role.menu.only("id", "title").all()
            menu_ids = [ru.id for ru in role_menus]

            for m in queryset:
                r = {}
                r["id"] = m.id
                r["title"] = "%s " % (m.title)
                if m.id in menu_ids:
                    r["selected"] = True
                else:
                    r["selected"] = False
                per_list.append(r)
            result["msg"] = per_list
        else:
            result = {"errcode": 1, "msg": "错误的参数"}
        return Response(result)

    def post(self, request, **kwargs):
        """ 修改 角色的用户信息 """
        result = {"errcode": 0, "msg": None}
        id = request.POST.get("id", None)
        menu_ids = request.POST.getlist("menus[]", [])
        role = Role.objects.filter(id=id).first()
        if role:
            role.menu.set(menu_ids)
            role.save()
            return Response(result)
        result["errcode"] = 1
        result["msg"] = "参数错误"
        return Response(result)