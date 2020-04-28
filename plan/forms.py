from django import forms
from .models import TimedTask
from assets.models import Assets


class CreateTimedTaskForm(forms.ModelForm):
    name = forms.CharField(
        label='任务名称',
        widget=forms.TextInput(
            attrs={"class": "form-control"}
        )
    )
    status = forms.ChoiceField(
        label='状态',
        choices=TimedTask.STATUS,
        widget=forms.Select(
            attrs={"class": "form-control "}
        )
    )
    account = forms.CharField(
        label='用户',
        widget=forms.TextInput(
            attrs={"class": "form-control", "value": "root"}
        )
    )
    host = forms.ModelChoiceField(
        label='选择主机',
        queryset=Assets.get_all(),
        widget=forms.Select(
            attrs={"class": "form-control selectpicker", "data-live-search": "true", "data-size": "5",
                   "data-width": "100%", "title": "请选择主机"}
        )
    )
    minute = forms.CharField(
        label='分',
        widget=forms.TextInput(
            attrs={"value": "*", "class": "form-control mywidth"}
        )
    )
    hour = forms.CharField(
        label='时',
        widget=forms.TextInput(
            attrs={"value": "*", "class": "form-control mywidth"}
        )
    )
    day = forms.CharField(
        label='日',
        widget=forms.TextInput(
            attrs={"value": "*", "class": "form-control mywidth"}
        )
    )
    month = forms.CharField(
        label='月',
        widget=forms.TextInput(
            attrs={"value": "*", "class": "form-control mywidth"}
        )
    )
    week = forms.CharField(
        label='周',
        widget=forms.TextInput(
            attrs={"value": "*", "class": "form-control mywidth"}
        )
    )
    code = forms.CharField(
        label='执行命令',
        widget=forms.Textarea(
            attrs={"class": "form-control", "cols": 40, "rows": 5}
        )
    )
    remark = forms.CharField(
        label='备注信息',
        required=False,
        widget=forms.Textarea(
            attrs={"class": "form-control", "cols": 40, "rows": 2}
        )
    )

    class Meta:
        model = TimedTask
        fields = ['name', 'host', 'status', 'account', 'minute', 'hour', 'day', 'month', 'week', 'code', 'remark']


class UpdateTimedTaskForm(forms.ModelForm):
    name = forms.CharField(
        label='任务名称',
        required=False,
        widget=forms.TextInput(
            attrs={"class": "form-control"}
        )
    )
    status = forms.ChoiceField(
        label='状态',
        choices=TimedTask.STATUS,
        widget=forms.Select(
            attrs={"class": "form-control select2 select2-hidden-accessible"}
        )
    )
    account = forms.CharField(
        label='用户',
        widget=forms.TextInput(
            attrs={"class": "form-control", "value": "root"}
        )
    )
    host = forms.ModelChoiceField(
        label='选择主机',
        queryset=Assets.get_all(),
        widget=forms.Select(
            attrs={"class": "form-control select2 select2-hidden-accessible"}
        )
    )
    minute = forms.CharField(
        label='分',
        widget=forms.TextInput(
            attrs={"value": "*", "class": "form-control mywidth"}
        )
    )
    hour = forms.CharField(
        label='时',
        widget=forms.TextInput(
            attrs={"value": "*", "class": "form-control mywidth"}
        )
    )
    day = forms.CharField(
        label='日',
        widget=forms.TextInput(
            attrs={"value": "*", "class": "form-control mywidth"}
        )
    )
    month = forms.CharField(
        label='月',
        widget=forms.TextInput(
            attrs={"value": "*", "class": "form-control mywidth"}
        )
    )
    week = forms.CharField(
        label='周',
        widget=forms.TextInput(
            attrs={"value": "*", "class": "form-control mywidth"}
        )
    )
    code = forms.CharField(
        label='执行命令',
        widget=forms.Textarea(
            attrs={"class": "form-control", "cols": 40, "rows": 5}
        )
    )
    remark = forms.CharField(
        label='备注信息',
        required=False,
        widget=forms.Textarea(
            attrs={"class": "form-control", "cols": 40, "rows": 2}
        )
    )

    class Meta:
        model = TimedTask
        fields = ['name', 'host', 'status', 'account', 'minute', 'hour', 'day', 'month', 'week', 'code', 'remark']


class CreateManyTaskForm(forms.ModelForm):
    status = forms.ChoiceField(
        label='状态',
        choices=TimedTask.STATUS,
        widget=forms.Select(
            attrs={"class": "form-control select2 select2-hidden-accessible"}
        )
    )
    account = forms.CharField(
        label='用户',
        widget=forms.Select(
            attrs={"class": "form-control select2 select2-hidden-accessible"}
        )
    )
    host = forms.ModelChoiceField(
        label='选择主机',
        queryset=Assets.get_all(),
        widget=forms.Select(
            attrs={"class": "form-control select2 select2-hidden-accessible"}
        )
    )
    code = forms.CharField(
        label='计划任务数据',
        help_text='任务名称(必填)|任务具体命令(必填)|备注信息(选填)',
        widget=forms.Textarea(
            attrs={"class": "form-control", "cols": 60, "rows": 5,
                   "placeholder": "任务名称(必填)|任务具体命令(必填)|备注信息(选填),中间必须以 | 分割,结尾回车换行"}
        )
    )

    class Meta:
        model = TimedTask
        fields = ['account', 'host', 'status', 'code']
