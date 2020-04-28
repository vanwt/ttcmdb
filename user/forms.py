from django import forms
from .models import User
# from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group, Permission


class CreateUserForm(forms.ModelForm):
    username = forms.CharField(
        label='用户名',
        max_length=50,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "名称",
                "title": "* required"
            }
        )
    )
    realname = forms.CharField(
        label='真实姓名',
        max_length=8,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "名称"
            }
        )
    )
    email = forms.CharField(
        label='邮箱',
        max_length=128,
        required=False,
        widget=forms.EmailInput(
            attrs={
                "class": "form-control", "placeholder": "邮件",
                "title": "* required"
            }
        )
    )
    password = forms.CharField(
        label='密码',
        max_length=128,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "密码"
            }
        )
    )

    phone = forms.CharField(
        label='手机号',
        max_length=11,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "手机"
            }
        )
    )
    info = forms.CharField(
        label='备注',
        required=False,
        max_length=500,
        widget=forms.Textarea(
            attrs={"cols": "40", "rows": "5", "maxlength": "200",
                   "class": "form-control", "placeholder": "备注"}
        )
    )

    class Meta:
        model = User
        fields = ['username', 'password', 'phone', 'realname', 'info', 'email', 'is_active',
                  'is_superuser', 'token', 'userid']
        # fields = '__all__'

    def clean_username(self):
        name = self.cleaned_data['username']
        user = User.get_by_name(name)
        if user:
            raise forms.ValidationError('用户名重复,请更换')
        return name

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if not phone.isdigit():
            raise forms.ValidationError('手机号必须为数字')
        if phone[0] != '1' or phone[1] in ['1', '2', '4', '9']:
            raise forms.ValidationError('请输入合法的手机号')
        return phone

    def clean_password(self):
        pwd = self.cleaned_data['password']
        if len(pwd) <= 6:
            raise forms.ValidationError('密码太短!')
        if pwd.isalpha() or pwd.isdigit():
            raise forms.ValidationError('密码必须由字母,数字，符号共同组成')
        return pwd


class UpdateUserForm(forms.ModelForm):
    username = forms.CharField(
        label='用户名',
        max_length=50,
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "名称",
                "title": "* required"
            }
        )
    )
    realname = forms.CharField(
        label='真实姓名',
        max_length=8,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "名称"
            }
        )
    )
    email = forms.CharField(
        label='邮箱',
        max_length=128,
        required=False,
        widget=forms.EmailInput(
            attrs={
                "class": "form-control", "placeholder": "邮件",
                "title": "* required"
            }
        )
    )
    phone = forms.CharField(
        label='手机号',
        max_length=11,
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "手机"
            }
        )
    )
    info = forms.CharField(
        label='备注',
        required=False,
        max_length=500,

        widget=forms.Textarea(
            attrs={"cols": "40", "rows": "5", "maxlength": "200",
                   "class": "form-control", "placeholder": "备注"}
        )
    )

    class Meta:
        model = User
        # 管理员显示全部，而用户只能看到部分
        fields = ['username', 'phone', 'realname', 'info', 'email', 'is_active', 'is_superuser', "is_staff"]


class UpdatePasswordForm(forms.ModelForm):
    old_password = forms.CharField(
        label='原来的密码',
        max_length=128,
        required=False,
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "原来密码"}
        )
    )
    new_password = forms.CharField(
        label='新密码',
        max_length=128,
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "新的密码"}
        )
    )
    new_pwd = forms.CharField(
        label='确认密码',
        max_length=128,
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "确认密码"}
        )
    )

    def clean_new_password(self):
        new_password = self.cleaned_data['new_password']
        if len(new_password) <= 6:
            raise forms.ValidationError('密码太短!')

        if new_password.isalpha() or new_password.isdigit():
            raise forms.ValidationError('密码必须由字母,数字，符号共同组成')
        return new_password

    class Meta:
        model = User
        fields = ['old_password', 'new_password', 'new_pwd']
