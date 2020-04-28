from django.db import models
# Create your models here.


class Log_Cron(models.Model):
    cron_id = models.IntegerField(verbose_name='id', blank=True, null=True, default=None)
    cron_user = models.CharField(max_length=50, verbose_name='操作用户', default=None)
    cron_name = models.CharField(max_length=100, verbose_name='名称', default=None)
    cron_content = models.CharField(max_length=100, default=None)
    cron_server = models.CharField(max_length=30, default=None)
    create_time = models.DateTimeField(auto_now_add=True, blank=True, null=True, verbose_name='执行时间')
    objects = models.Manager
    class Meta:
        db_table = 'log_cron'
        verbose_name = '任务配置操作记录表'
        verbose_name_plural = '任务配置操作记录表'
