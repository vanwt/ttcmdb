from django.db import models
from assets.models import Assets
from user.models import User
from django.shortcuts import Http404


# Create your models here.

class TimedTask(models.Model):
    STATUS = [
        (0, '未激活'), (1, '激活'),
    ]
    name = models.CharField(verbose_name='任务名称', max_length=128, blank=True, null=True, unique=True)
    host = models.ForeignKey(Assets, verbose_name='选择运行主机', related_name='plan', null=True, on_delete=models.SET_NULL,
                             blank=True, db_constraint=False)
    minute = models.CharField(verbose_name='分', max_length=32, default='*', blank=True)
    hour = models.CharField(verbose_name='时', max_length=32, default='*', blank=True)
    account = models.CharField(verbose_name='使用用户', max_length=32, blank=True)
    day = models.CharField(verbose_name='日', max_length=32, default='*', blank=True)
    month = models.CharField(verbose_name='月', max_length=32, default='*', blank=True)
    week = models.CharField(verbose_name='周', max_length=32, default='*', blank=True)
    code = models.CharField(verbose_name='任务执行内容', max_length=2500, blank=True)
    status = models.PositiveIntegerField(verbose_name='状态', choices=STATUS, blank=True)
    execution_status = models.PositiveIntegerField(verbose_name='执行状态',
                                                   choices=((1, '正在执行'), (2, '执行成功'), (3, '执行失败'), (4, '未执行')),
                                                   null=True, blank=True)
    remark = models.TextField(verbose_name='任务描述', null=True, blank=True)
    create_user = models.ForeignKey(User, verbose_name='创建用户', on_delete=models.SET_NULL, null=True,
                                    db_constraint=False)
    create_time = models.DateField(auto_now_add=True, verbose_name="创建时间")
    change_time = models.DateField(auto_now_add=True, verbose_name="修改时间")
    objects = models.Manager

    class Meta:
        db_table = 'timedtask'
        verbose_name = '定时任务'
        verbose_name_plural = verbose_name

    @staticmethod
    def get_by_id(id):
        try:
            c = TimedTask.objects.get(id=id)
            return c
        except TimedTask.DoesNotExist:
            return None

    @staticmethod
    def get_all():
        return TimedTask.objects.all()

    def get_by_id_only_status(id):
        try:
            task = TimedTask.objects.filter(id=id).only('status')[0]
            return task.status
        except TimedTask.DoesNotExist:
            return None
        except IndexError:
            return None
