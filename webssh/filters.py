import django_filters
from django import forms
from user.models import User
from assets.models import Assets
from .models import SessionLog


class SSHLogFilter(django_filters.FilterSet):
    user = django_filters.ChoiceFilter(
        choices=[[u.realname, u.realname] for u in User.get_all()], label="用户",
        widget=forms.Select(attrs={'class': "form-control selectpicker", "data-live-search": "true", "data-size": "5",
                                   "data-width": "100%"}))
    host = django_filters.ChoiceFilter(
        choices=Assets.get_all_ip(), label="主机",
        widget=forms.Select(attrs={'class': "form-control selectpicker", "data-live-search": "true", "data-size": "5",
                                   "data-width": "100%"}))
    create_time = django_filters.DateTimeFilter(
        label="开始时间", field_name="create_time", lookup_expr="exact",
        widget=forms.DateTimeInput(attrs={'class': "form-control input-sm", 'placeholder': 'YYYY-MM-DD hh:mm'}))

    class Meta:
        model = SessionLog
        fields = ["user", "host", "create_time"]
