from django.db import models
from django.shortcuts import Http404
import datetime


# Create your models here.

class IDC(models.Model):
    """IDC资产信息"""

    IDC_OPERATOR = (
        (0, u"电信"),
        (1, u"联通"),
        (2, u"移动"),
        (3, u"铁通"),
        (4, u"小带宽"),
    )
    name = models.CharField(max_length=128, unique=True, verbose_name="机房名称")
    linkphone = models.CharField(max_length=16, blank=True, null=True, verbose_name="联系电话")
    address = models.CharField(max_length=128, blank=True, null=True, verbose_name="机房地址")
    network_segment = models.TextField(blank=True, null=True, verbose_name="网段")
    bandwidth = models.CharField(max_length=64, blank=True, null=True, verbose_name="机房带宽")
    operator = models.PositiveIntegerField(verbose_name="运营商", choices=IDC_OPERATOR, blank=True, null=True)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    change_time = models.DateTimeField(auto_now=True, verbose_name="修改时间")

    objects = models.Manager

    class Meta:
        db_table = 'idc'
        verbose_name_plural = verbose_name = 'IDC资产表'

    def __str__(self):
        return self.name

    @staticmethod
    def get_all():
        return IDC.objects.all()

    @staticmethod
    def get_by_id(id):
        try:
            return IDC.objects.get(id=id)
        except IDC.DoesNotExist:
            return None

    @staticmethod
    def get_by_name(name):
        try:
            return IDC.objects.get(name=name)
        except IDC.DoesNotExist:
            return None


class Tags(models.Model):
    """资产标签"""

    name = models.CharField(max_length=64, blank=True, null=True, unique=True, verbose_name="标签")
    create_time = models.DateField(auto_now_add=True, verbose_name="创建时间")
    objects = models.Manager

    class Meta:
        db_table = "tags"
        verbose_name = "资产标签表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    @staticmethod
    def get_all():
        return Tags.objects.all()

    @staticmethod
    def get_by_id(id):
        try:
            return Tags.objects.get(id=id)
        except Tags.DoesNotExist:
            return None
