import uuid
from django.db import models
from user.models import User


class Assets(models.Model):
    """ 资产信息表"""
    ASSET_STATUS = (
        (0, '下线'), (1, '在线'), (2, '故障中'), (3, '未使用'), (4, '未知')
    )
    SERVER_TYPE_CHOICES = (
        (1, '物理机'),
        (2, '虚拟机'),
        (3, '云主机'),
    )
    is_pass_choices = (
        (0, "失败"), (1, "通"), (2, "错误")
    )
    # 定义uuid 为自增主键
    id = models.UUIDField(verbose_name="ID", primary_key=True, default=uuid.uuid4, editable=False)
    ip = models.GenericIPAddressField(verbose_name="IP", unique=True, null=True, blank=True, db_index=True)
    # 主要
    status = models.PositiveIntegerField(verbose_name='设备状态', default=1, choices=ASSET_STATUS)
    asset_type = models.PositiveIntegerField(verbose_name="资产类型", choices=SERVER_TYPE_CHOICES)
    system = models.CharField(verbose_name="操作系统", max_length=32, blank=True, null=True)

    # 关联
    project = models.ForeignKey('project.Project', null=True, blank=True, on_delete=models.SET_NULL,
                                verbose_name="所属项目", db_constraint=False)
    idc = models.ForeignKey("assets.IDC", verbose_name="所属机房", null=True, blank=True, on_delete=models.SET_NULL,
                            db_constraint=False)
    tags = models.ManyToManyField("assets.Tags", blank=True, verbose_name="标签", db_constraint=False)

    system_users = models.ManyToManyField("assets.SystemUser", verbose_name="系统用户", blank=True, related_name="assets",
                                          db_constraint=False)

    # 配置
    is_del = models.BooleanField(verbose_name='是否删除', null=True, default=False, blank=True)
    is_active = models.BooleanField(verbose_name='激活', default=True, null=True, blank=True)
    is_pass = models.BooleanField(verbose_name="可连接", default=True, null=True, blank=True)
    # 软件信息
    sshuser = models.CharField(max_length=64, null=True, blank=True, verbose_name='SSH用户')
    sshport = models.CharField(max_length=5, null=True, blank=True, default=22, verbose_name='SSH端口')
    sshpwd = models.CharField(max_length=128, null=True, blank=True, verbose_name='SSH密码')
    ftp_port = models.CharField(max_length=5, null=True, blank=True, verbose_name='FTP端口')

    # 硬件信息
    cpu = models.CharField(max_length=128, null=True, blank=True, verbose_name='CPU型号')
    logical_cpu = models.PositiveIntegerField(null=True, blank=True, verbose_name='逻辑CPU数')
    ram = models.IntegerField('内存容量', null=True, blank=True)
    disk = models.FloatField('磁盘容量', null=True, blank=True)

    remark = models.TextField(verbose_name='备注信息')
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    change_time = models.DateTimeField(verbose_name='更新时间', auto_now=True)

    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, db_constraint=False)
    objects = models.Manager()

    class Meta:
        permissions = (
            ("asset_export", "能否导出资产表"), ("asset_import", "能否导入资产表"),
        )
        db_table = 'assets'
        verbose_name_plural = verbose_name = '资产表'

    def __str__(self):
        return self.ip

    @classmethod
    def get_all(cls):
        return cls.objects.all()

    @staticmethod
    def get_nums():
        return Assets.objects.all().count()

    @staticmethod
    def get_by_id(id):
        try:
            if type(id) == list:
                id = int(id[0])
            asset = Assets.objects.get(id=id)
            return asset
        except Assets.DoesNotExist:
            return None

    @staticmethod
    def get_all_ip():
        assets = Assets.objects.only("ip").all()
        # return assets
        return [(ass.ip, ass.ip) for ass in assets]

    @staticmethod
    def get_string_servers():
        physical = Assets.objects.only('id').filter(asset_type=1).count()
        virtual = Assets.objects.only('id').filter(asset_type=2).count()
        cloud = Assets.objects.only('id').filter(asset_type=3).count()
        l = [physical, virtual, cloud]
        return str(l)


class DelAssetModel(models.Model):
    SERVER_TYPE_CHOICES = (
        (1, '物理机'),
        (2, '虚拟机'),
        (3, '云主机'),
    )
    ip = models.GenericIPAddressField(verbose_name='IP', max_length=128, null=True, blank=True)

    # 服务器信息
    asset_type = models.PositiveIntegerField(choices=SERVER_TYPE_CHOICES, null=True, blank=True, verbose_name="资产类型")
    sshuser = models.CharField(max_length=64, null=True, blank=True, verbose_name='SSH用户')
    sshpwd = models.CharField(max_length=128, null=True, blank=True, verbose_name='SSH密码')
    cpu = models.CharField(max_length=128, null=True, blank=True, verbose_name='CPU型号')
    logical_cpu = models.PositiveIntegerField(null=True, blank=True, verbose_name='逻辑CPU数')
    delete_time = models.DateTimeField(verbose_name='删除时间', auto_now_add=True, null=True, blank=True)

    class Meta:
        db_table = 'assets_del'
        verbose_name = '资产删除登记表'
        verbose_name_plural = verbose_name
