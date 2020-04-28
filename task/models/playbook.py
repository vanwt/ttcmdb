from django.db import models


class AnsiblePlaybook(models.Model):
    playbook_name = models.CharField(max_length=100, verbose_name='剧本名称', unique=True)
    playbook_file = models.FileField(upload_to='playbooks/', null=True, blank=True)
    playbook_content = models.TextField(verbose_name='剧本内容', null=True)
    playbook_user = models.ForeignKey('user.User', verbose_name='添加人员', on_delete=models.SET_NULL, null=True,
                                      db_constraint=False)
    playbook_time = models.DateTimeField(auto_now_add=True, verbose_name='添加日期')
    playbook_desc = models.TextField(verbose_name='剧本描述', null=True, blank=True)
    objects = models.Manager

    class Meta:
        db_table = 'ansible_playbook'
        verbose_name = 'Ansible剧本表'
        verbose_name_plural = 'Ansible剧本表'


class AnsiblePlaybookLog(models.Model):
    playbook_user = models.ForeignKey("user.User", on_delete=models.SET_NULL, null=True, db_constraint=False,
                                      verbose_name='操作用户')
    playbook_name = models.CharField(max_length=100, verbose_name='剧本名称')
    playbook_result = models.TextField(verbose_name='执行结果')
    playbook_datetime = models.DateTimeField(auto_now_add=True, verbose_name='执行时间')

    class Meta:
        db_table = 'ansible_playbook_log'
        verbose_name = 'Playbook执行记录表'
        verbose_name_plural = 'Playbook执行记录表'
