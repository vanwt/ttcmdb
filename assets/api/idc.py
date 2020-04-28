from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from ..models import IDC
from .. import serializers
# from . import save_log


class IdcViewset(ModelViewSet):
    queryset = IDC.objects.all()
    serializer_class = serializers.IdcSerializers

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        ip = request.META.get('REMOTE_HOST')
        msg = "删除IDC %s" % instance.name
        # save_log.delay(request.user.realname, action='del', resource='Assets资产表', operating=msg, ip=ip)
        try:
            self.perform_destroy(instance)
        except Exception as e:
            return Response({"code": 400, "msg": "删除失败！" + str(e)})
        return Response({"code": 200, "msg": "删除成功！"})
