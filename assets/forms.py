from django import forms
from .models import (Assets, IDC, Tags, SystemUser)
from project.models import Project


class AssetForm(forms.ModelForm):
    """资产创建表单"""
    asset_type = forms.ChoiceField(
        label='资产类型',
        choices=Assets.SERVER_TYPE_CHOICES,
        widget=forms.Select(
            attrs={
                "class": "form-control select2 select2-hidden-accessible"
            }
        )
    )
    status = forms.ChoiceField(
        label='资产状态',
        choices=Assets.ASSET_STATUS,
        widget=forms.Select(
            attrs={"class": "form-control select2 select2-hidden-accessible"}
        )
    )
    ip = forms.GenericIPAddressField(
        label='管理IP',
        widget=forms.TextInput(
            attrs={"class": "form-control"}
        )
    )
    idc = forms.ModelChoiceField(
        label='选择机房',
        required=False,
        queryset=IDC.get_all(),
        widget=forms.Select(
            attrs={"class": "form-control "}
        )
    )
    project = forms.ModelChoiceField(
        label='所属项目',
        required=False,
        queryset=Project.get_all(),
        widget=forms.Select(
            attrs={"class": "form-control", "data-live-search": "true", "data-size": "3",
                   "data-width": "100%"}
        )
    )
    tags = forms.ModelMultipleChoiceField(
        label='标签',
        required=False,
        queryset=Tags.get_all(),
        widget=forms.SelectMultiple(
            attrs={"class": "form-control dual_select"}
        )
    )
    remark = forms.CharField(
        label='备注信息',
        required=False,
        widget=forms.Textarea(
            attrs={"class": "form-control", "cols": 40, "rows": 5}
        )
    )
    system = forms.CharField(
        label='系统',
        required=False,
        widget=forms.TextInput(
            attrs={"class": "form-control"}
        )
    )
    sshuser = forms.CharField(
        label='登录用户',
        required=False,
        widget=forms.TextInput(
            attrs={"class": "form-control"}
        )
    )
    sshpwd = forms.CharField(
        label='登录密码',
        required=False,
        widget=forms.TextInput(
            attrs={"class": "form-control"}
        )
    )
    sshport = forms.CharField(
        label='端口',
        required=False,
        widget=forms.NumberInput(
            attrs={"class": "form-control", "value": "22"}
        )
    )

    mysql_user = forms.CharField(
        label='数据库用户',
        required=False,
        widget=forms.TextInput(
            attrs={"class": "form-control", "value": "root"}
        )
    )
    mysql_pwd = forms.CharField(
        label='数据库密码',
        required=False,
        widget=forms.TextInput(
            attrs={"class": "form-control"}
        )
    )
    ftp_port = forms.CharField(
        label='FTP端口',
        required=False,
        widget=forms.NumberInput(
            attrs={"class": "form-control"}
        )
    )

    class Meta:
        model = Assets
        fields = ['asset_type', 'status', "system", "system_users", "sshuser", "sshpwd", "sshport", "mysql_user",
                  "mysql_pwd", "ftp_port", 'ip', 'idc', 'project', 'system', 'sshuser',
                  'sshpwd', 'sshport', 'mysql_user', 'mysql_pwd', 'ftp_port', 'tags', 'remark', 'is_active']


class CreateSystemUserForm(forms.ModelForm):
    username = forms.CharField(
        label='推送用户',
        widget=forms.TextInput(
            attrs={"class": "form-control"}
        )
    )
    password = forms.CharField(
        label='推送用户密码',
        widget=forms.TextInput(
            attrs={"class": "form-control"}
        )
    )
    group = forms.CharField(
        label='用户组',
        required=False,
        widget=forms.TextInput(
            attrs={"class": "form-control"}
        )
    )

    class Meta:
        model = SystemUser
        fields = ['username', 'password', "group"]

    def clean_username(self):
        username = self.cleaned_data['username']
        if SystemUser.objects.filter(username=username).count() >= 1:
            raise forms.ValidationError("该用户已存在")
        return username


class UpdateSystemUserForm(forms.ModelForm):
    username = forms.CharField(
        label='推送用户',
        disabled=True,
        widget=forms.TextInput(
            attrs={"class": "form-control"}
        )
    )
    password = forms.CharField(
        label='推送用户密码',
        disabled=True,
        widget=forms.TextInput(
            attrs={"class": "form-control"}
        )
    )
    group = forms.CharField(
        label='用户组',
        required=False,
        widget=forms.TextInput(
            attrs={"class": "form-control"}
        )
    )

    class Meta:
        model = SystemUser
        fields = ['username', 'password', "group"]
