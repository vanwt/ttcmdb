import django_filters
from django import forms
from .models import AnsibleModuleLog, AnsiblePlaybookLog, RunRoleLog
from user.models import User


class ModuleLogFilter(django_filters.FilterSet):
    ans_user = django_filters.ModelChoiceFilter(
        queryset=User.get_all(), label="用户",
        widget=forms.Select(attrs={'class': "form-control selectpicker", "data-live-search": "true", "data-size": "5",
                                   "data-width": "100%"}))
    ans_module = django_filters.CharFilter(
        label="模块名",
        lookup_expr="icontains",
        field_name="ans_module",
        widget=forms.TextInput(attrs={'class': "form-control input-sm"})
    )
    ans_server = django_filters.CharFilter(
        label="IP",
        lookup_expr="icontains",
        field_name="ans_server",
        widget=forms.TextInput(attrs={'class': "form-control input-sm"})
    )
    ans_datetime__lte = django_filters.DateTimeFilter(
        field_name="ans_datetime", lookup_expr="lte",
        label="Date小于",
        widget=forms.DateTimeInput(attrs={'class': "form-control input-sm", 'placeholder': 'YYYY-MM-DD hh:mm'}))
    ans_datetime__gte = django_filters.DateTimeFilter(
        field_name="ans_datetime",
        lookup_expr="gte",
        label="Date大于",
        widget=forms.DateTimeInput(attrs={'class': "form-control input-sm", 'placeholder': 'YYYY-MM-DD hh:mm'}))

    class Meta:
        model = AnsibleModuleLog
        fields = ["ans_module", "ans_user", "ans_server", "ans_datetime"]


class PlaybookLogFilter(django_filters.FilterSet):
    playbook_user = django_filters.ModelChoiceFilter(
        queryset=User.get_all(), label="用户",
        widget=forms.Select(attrs={'class': "form-control selectpicker", "data-live-search": "true", "data-size": "5",
                                   "data-width": "100%"})
    )
    playbook_datetime__lte = django_filters.DateTimeFilter(
        field_name="playbook_datetime", lookup_expr="lte",
        label="Date小于",
        widget=forms.DateTimeInput(attrs={'class': "form-control input-sm", 'placeholder': 'YYYY-MM-DD hh:mm'})
    )
    playbook_datetime__gte = django_filters.DateTimeFilter(
        field_name="playbook_datetime", lookup_expr="gte",
        label="Date大于",
        widget=forms.DateTimeInput(attrs={'class': "form-control input-sm", 'placeholder': 'YYYY-MM-DD hh:mm'})
    )

    class Meta:
        model = AnsiblePlaybookLog
        fields = ["playbook_user", "playbook_datetime__lte", "playbook_datetime__gte"]


class RoleLogFilter(django_filters.FilterSet):
    role_user = django_filters.ModelChoiceFilter(
        queryset=User.get_all(), label="用户",
        widget=forms.Select(attrs={'class': "form-control selectpicker", "data-live-search": "true", "data-size": "5",
                                   "data-width": "100%"})
    )
    role_datetime__lte = django_filters.DateTimeFilter(
        field_name="role_datetime", lookup_expr="lte",
        label="Date小于",
        widget=forms.DateTimeInput(attrs={'class': "form-control input-sm", 'placeholder': 'YYYY-MM-DD hh:mm'})
    )
    role_datetime__gte = django_filters.DateTimeFilter(
        field_name="role_datetime", lookup_expr="gte",
        label="Date大于",
        widget=forms.DateTimeInput(attrs={'class': "form-control input-sm", 'placeholder': 'YYYY-MM-DD hh:mm'})
    )

    class Meta:
        model = RunRoleLog
        fields = ["role_user", "role_datetime__lte", "role_datetime__gte"]
