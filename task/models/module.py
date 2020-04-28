from django.db import models
from user.models import User


# Create your models here.
class AnsibleModuleLog(models.Model):
    ans_user = models.ForeignKey(User, on_delete=models.SET_NULL, db_constraint=False, verbose_name='操作用户', null=True)

    ans_module = models.CharField(max_length=100, verbose_name='模块名称')
    ans_args = models.CharField(max_length=500, blank=True, null=True, verbose_name='模块参数', default=None)
    ans_server = models.TextField(verbose_name='服务器')
    ans_result = models.TextField(verbose_name='执行结果')
    ans_datetime = models.DateTimeField(auto_now_add=True, verbose_name='执行时间')

    class Meta:
        db_table = 'ans_module_log'
        verbose_name = 'Ansible模块执行记录表'
        verbose_name_plural = verbose_name
