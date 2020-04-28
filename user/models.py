# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib import auth
import uuid


# 继承Django自带的user表


class User(AbstractUser):
    """用户表"""
    id = models.UUIDField(verbose_name="用户ID", default=uuid.uuid4, primary_key=True, editable=False)
    password = models.CharField('password', max_length=128, blank=True, null=True)
    phone = models.CharField('手机号', max_length=11, null=False)
    realname = models.CharField('真实姓名', max_length=32, null=False)
    is_active = models.BooleanField(verbose_name='是否激活', default=True, null=True)

    avatar = models.CharField(verbose_name='用户头像', max_length=255, default='/static/users-img/admin.png', null=True)
    info = models.CharField(verbose_name='介绍', null=True, max_length=100)

    token = models.CharField(verbose_name="钉钉唯一标识符", max_length=128, blank=True)
    userid = models.CharField(verbose_name="钉钉用户id", max_length=128, blank=True, null=True)
    create_time = models.DateTimeField(verbose_name='创建时间', auto_created=True, null=True)
    change_time = models.DateTimeField(verbose_name='更新时间', auto_now_add=True, null=True)

    class Meta:
        db_table = 'user'
        verbose_name = '用户表'
        verbose_name_plural = verbose_name

    def __str__(self):
        if self.realname:
            return self.realname
        else:
            return self.username

    @classmethod
    def get_all(cls):
        return cls.objects.all()

    @staticmethod
    def get_by_name(name):
        try:
            user = User.objects.get(username=name)
        except User.DoesNotExist:
            user = None
        return user

    # 获取用户数量
    @staticmethod
    def get_nums():
        return User.objects.all().count()

    # 检查用户名密码是否正确 在forms中
    @staticmethod
    def check_user_password(account, password):
        if account.isdigit():
            user = auth.authenticate(phone=account, password=password)
        else:
            user = auth.authenticate(username=account, password=password)
        if not user:
            return None
        return user

    @staticmethod
    def get_by_id(id):
        try:
            user = User.objects.get(id=id)
        except User.DoesNotExist:
            return None
        return user


class UrlPermission(models.Model):
    METHODS = (
        ("GET", "GET"), ("POST", "POST"), ("PUT", "PUT"), ("DELETE", "DELETE"), ("ALL", "ALL")
    )
    title = models.CharField(max_length=64, blank=True)
    url = models.CharField(max_length=128, null=True, blank=True, help_text="url与method 联合唯一")
    status = models.BooleanField(default=True, blank=True)
    is_absolute = models.BooleanField(default=True, blank=True, verbose_name="绝对匹配(默认:模糊匹配)")

    method = models.CharField(max_length=32, choices=METHODS, default="GET", blank=True)
    objects = models.Manager

    class Meta:
        db_table = "permission"
        unique_together = ("url", "method")
        verbose_name = "url权限表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "<%s : %s>" % (self.title, self.get_method_display())


class Menu(models.Model):
    """ 菜单权限表 """
    title = models.CharField(max_length=64, blank=True)
    status = models.BooleanField(default=True, blank=True)
    # 兼容vue
    icon = models.CharField(verbose_name="图标", null=True, blank=True, max_length=64)
    name = models.CharField(verbose_name="别名", null=True, blank=True, max_length=32)
    path = models.CharField(verbose_name="路径", max_length=128, null=True, blank=True)
    url = models.CharField(verbose_name="url", max_length=128, null=True, blank=True)
    objects = models.Manager

    class Meta:
        db_table = "menu"
        verbose_name = "菜单"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class Role(models.Model):
    """ 角色表 """
    title = models.CharField(max_length=64, blank=True)
    menu = models.ManyToManyField(Menu, related_name="role", db_constraint=False, blank=True)
    permission = models.ManyToManyField(UrlPermission, related_name="role", db_constraint=False, blank=True)
    users = models.ManyToManyField("user.User", related_name="roles", db_constraint=False, blank=True)
    status = models.BooleanField(default=True, blank=True)
    objects = models.Manager

    class Meta:
        db_table = "role"
        verbose_name = "角色"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title
