from django.db import models
from assets.models import Assets, SystemUser
import uuid


class SessionLog(models.Model):
    """
    会话连接记录表
    日志和在线都使用此表
    每个key必须唯一
    """
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    session_state = ((0, '已结束'), (1, '正在进行'))
    host = models.GenericIPAddressField(verbose_name='连接主机', null=True)
    user = models.CharField(verbose_name='使用用户', max_length=64, null=True)
    ssh_user = models.CharField(verbose_name='ssh用户', max_length=128, null=True, blank=True)
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True, null=True)
    end_time = models.DateTimeField(verbose_name='结束时间', auto_now=True, null=True)
    status = models.PositiveSmallIntegerField(verbose_name='状态', choices=session_state, default=1, null=True,
                                              blank=True)
    used = models.BooleanField(verbose_name="是否连接过", default=False, null=True)
    link_ip = models.GenericIPAddressField(verbose_name='操作IP', null=True, blank=True)
    objects = models.Manager

    class Meta:
        permissions = (
            ("run_webssh", "是否能执行远程主机"),
        )
        db_table = 'ssh_session_log'
        verbose_name = '会话连接记录表'
        verbose_name_plural = verbose_name

    @staticmethod
    def get_by_id(id):
        try:
            return SessionLog.objects.get(id=id)
        except SessionLog.DoesNotExist:
            return None

    # 反回这个key的对象
    @staticmethod
    def get_by_skey(skey):
        try:
            return SessionLog.objects.get(id=skey)
        except SessionLog.DoesNotExist:
            return None

    @staticmethod
    def get_all():
        return SessionLog.objects.filter(status=0)

    @staticmethod
    def get_all_by_user(user):
        # 查询当前用户可见的数据
        return SessionLog.objects.filter(user=user.realname, status=0)


class CodeLog(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    addtime = models.DateTimeField(auto_now=True)
    connection = models.ForeignKey(SessionLog, related_name="log", on_delete=models.DO_NOTHING, null=True,
                                   db_constraint=False)  # 只创建逻辑关联数据
    command = models.TextField()
    result = models.TextField(null=True)

    objects = models.Manager

    class Meta:
        db_table = "code_log"
