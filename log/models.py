from django.db import models


class Loginlog(models.Model):
    """用户每次登录存储"""
    login_status = ((0, '失败'), (1, '成功'))
    user = models.CharField(verbose_name='用户名', max_length=128)
    login_time = models.DateTimeField(auto_created=True, verbose_name='登录时间')
    ip = models.GenericIPAddressField(verbose_name='登录IP', null=True)
    status = models.BooleanField(verbose_name='登录状态', choices=login_status)

    class Meta:
        db_table = 'login_log'
        verbose_name = '登录日志'


class OperatingLog(models.Model):
    action_choices = (
        ('add', '增加'), ('view', '查看'), ('change', '修改'), ('del', '删除')
    )
    user = models.CharField(max_length=128, verbose_name='操作用户', editable=False)
    action = models.CharField(verbose_name='动作', choices=action_choices, max_length=32, editable=False)
    resource = models.CharField(verbose_name='资源类型', max_length=32, editable=False)
    operating = models.CharField(verbose_name='执行操作', max_length=256, editable=False)
    ip = models.GenericIPAddressField(verbose_name='远端地址', null=True)
    create_time = models.DateTimeField(verbose_name='创建时间', auto_created=True)

    class Meta:
        db_table = 'operating_log'
        verbose_name = '操作日志'
