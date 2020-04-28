from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponseRedirect
from user.models import UrlPermission


class AccessControlMiddleware(MiddlewareMixin):

    def process_request(self, request):
        unlogin_exclude = (
            '/user/login/',
            "/user/logout/",
            "/user/update/",
            "/admin/",
            "/403/", "/favicon.ico/")

        login_exclude = (
            "/user/info/", "/user/password/update/"
        )
        if request.user.is_superuser:
            return None
        if request.path in unlogin_exclude:
            return None
        if request.user.is_anonymous:
            return HttpResponseRedirect("/user/login/")
        if request.path in login_exclude:
            return None

        path = request.path
        if "?" in path:
            path = path.split("?")[0]

        roles = request.user.roles.filter(status=True)
        # 得到所有的访问权限
        permissions = UrlPermission.objects.none()
        for role in roles:
            permissions |= role.permission.only("title", "method").filter(status=True)

        for p in permissions:
            # 必须路径匹配,然后 url 必须
            if p.url in path:
                if p.url == path and path in ["/", "/index/"]:
                    return None
                if p.url != "/" and (p.method == request.method or p.get_method_display() == "ALL"):
                    return None
        else:
            return HttpResponseRedirect("/403/")
