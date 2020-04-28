from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponseRedirect


class CheckLoginMiddleware(MiddlewareMixin):

    def process_request(self, request):
        # print(request.user.get_all_permissions())
        exclude = ["/user/signup/", "/user/dingding/", '/user/login/', "/user/logout/", "/user/update/",
                   "/ssh/chainssh/", "/xs-backstage/",
                   "/ftp/dd-run/", "/api/v1/reset/fpd/"]
        # 如果没有user就跳转到登录
        # 排除
        pc = [e for e in exclude if e in request.path]
        if request.user.is_authenticated == False and pc == []:
            return HttpResponseRedirect('/user/login/')
        if request.user.is_authenticated and not request.user.realname and "/user/update/" not in request.path:
            # 如果有登录，如果没有真实姓名，第一次登陆要跳转到修改信息哪里改名字
            url = '/user/update/' + str(request.user.id) + "/?next=" + "/index/"
            return HttpResponseRedirect(url)
