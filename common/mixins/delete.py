from rest_framework.response import Response

class MyDeleteMixin():
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            self.perform_destroy(instance)
        except Exception as e:
            return Response({"code": 400, "msg": "删除失败！" + str(e)})
        return Response({"code": 200, "msg": "删除成功！"})
