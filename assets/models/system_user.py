import datetime
import uuid
from django.db import models
from user.models import User


class SystemUser(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4, )
    username = models.CharField(verbose_name='登录用户名', max_length=64, null=True, blank=True)
    password = models.CharField(verbose_name='登录密码', max_length=255, null=True, blank=True)
    group = models.CharField(verbose_name="组", max_length=128, null=True, blank=True)
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    creator = models.ForeignKey(User, verbose_name='创建者', on_delete=models.SET_NULL, db_constraint=False, null=True,
                                blank=True)

    objects = models.Manager

    class Meta:
        db_table = 'system_user'
        verbose_name = '系统用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username

    @staticmethod
    def get_by_id(id):
        try:
            return SystemUser.objects.get(id=id)
        except SystemUser.DoesNotExist:
            return None

    @staticmethod
    def get_all():
        return SystemUser.objects.all()


class PushSystemUserLog(models.Model):
    """
    服务器用户推送记录 & 日志
    """
    username = models.CharField(max_length=128, verbose_name="推送用户", null=True, blank=True)
    host = models.GenericIPAddressField(verbose_name="推送主机")
    pusher = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='推送者', db_constraint=False,
                               blank=True)
    push_time = models.DateTimeField(auto_now_add=datetime.datetime.now(), verbose_name='推送时间')

    objects = models.Manager

    class Meta:
        db_table = 'push_user_log'
        verbose_name = '系统用户推送表'
        verbose_name_plural = verbose_name

    @staticmethod
    def get_by_id(id):
        try:
            return PushSystemUserLog.objects.get(id=id)
        except PushSystemUserLog.DoesNotExist:
            return None
