from django.db import models
from django.http.response import Http404
import uuid


class Project(models.Model):
    """项目资产信息"""
    id = models.UUIDField(verbose_name="ID", primary_key=True, default=uuid.uuid4, editable=False)
    project_name = models.CharField(max_length=128, verbose_name="项目名称")
    project_desc = models.TextField(blank=True, null=True, verbose_name="项目说明")

    auth_users = models.ManyToManyField("user.User", blank=True, verbose_name="授权用户", related_name="projects",
                                        db_constraint=False)
    creator = models.ForeignKey("user.User", blank=True, null=True, verbose_name='创建者', on_delete=models.SET_NULL,
                                db_constraint=False)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    change_time = models.DateTimeField(auto_now=True, verbose_name="修改时间")
    objects = models.Manager

    class Meta:
        db_table = "project"
        verbose_name = "项目表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.project_name

    @staticmethod
    def get_all():
        return Project.objects.all()

    @staticmethod
    def get_by_id(id):
        try:
            return Project.objects.get(id=id)
        except Project.DoesNotExist:
            raise Http404

    @staticmethod
    def get_by_name(name):
        try:
            return Project.objects.get(project_name=name)
        except Project.DoesNotExist:
            return None
