from django.db import models


class AnsibleRole(models.Model):
    role_name = models.CharField(max_length=100, verbose_name='role名称', unique=True)
    role_file = models.FileField(upload_to='roles/')
    role_user = models.ForeignKey("user.User", verbose_name='添加人员', on_delete=models.SET_NULL, null=True,
                                  db_constraint=False)
    role_time = models.DateTimeField(auto_now_add=True, verbose_name='添加日期')
    role_desc = models.TextField(verbose_name='role描述', null=True, blank=True)
    objects = models.Manager

    class Meta:
        db_table = 'ansible_role'
        verbose_name = 'AnsibleRole表'
        verbose_name_plural = 'AnsibleRole表'

    @staticmethod
    def get_name_by_id(rid):
        try:
            name = AnsibleRole.objects.only("role_name").get(id=rid)
            return name
        except AnsibleRole.DoesNotExist:
            return None


class RunRoleScript(models.Model):
    """
    用于存储执行role的脚本
    """
    r_name = models.CharField(verbose_name="脚本名", max_length=128, unique=True, blank=True)
    r_content = models.TextField(verbose_name="脚本内容/.yml", null=True, blank=True)
    creator = models.ForeignKey("user.User", verbose_name="创建用户", null=True, blank=True, on_delete=models.SET_NULL)
    change_time = models.DateTimeField(verbose_name="最后修改", auto_now_add=True, blank=True)
    objects = models.Manager

    class Meta:
        db_table = "run_role_script"
        verbose_name = "AnsibleRole执行脚本表"

    @staticmethod
    def get_by_id(rid, related=False):
        try:
            if related:
                script = RunRoleScript.objects.select_related("creator").get(id=rid)
            else:
                script = RunRoleScript.objects.get(id=rid)
            return script
        except RunRoleScript.DoesNotExist:
            return None

    def get_by_name(name):
        try:
            script = RunRoleScript.objects.get(r_name=name)
            return script
        except RunRoleScript.DoesNotExist:
            return None


class RunRoleLog(models.Model):
    role_user = models.ForeignKey("user.User", on_delete=models.SET_NULL, verbose_name='操作用户', null=True,
                                  db_constraint=False)
    role_name = models.CharField(max_length=100, verbose_name='剧本名称')
    role_result = models.TextField(verbose_name='执行结果')
    role_datetime = models.DateTimeField(auto_now_add=True, verbose_name='执行时间')

    class Meta:
        db_table = 'ansible_role_log'
        verbose_name = 'Role执行记录表'
        verbose_name_plural = 'Role执行记录表'
