import django_filters
from django import forms
from .models import TimedTask
from assets.models import Assets


class PlanFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(
        field_name="name", lookup_expr="icontains", label="任务名",
        widget=forms.TextInput(attrs={'class': "form-control input-sm"}))
    host = django_filters.ModelChoiceFilter(
        queryset=Assets.get_all(), label="主机",
        widget=forms.Select(attrs={'class': "form-control selectpicker", "data-live-search": "true", "data-size": "5",
                                   "data-width": "100%"})
    )
    create_time__lte = django_filters.DateTimeFilter(
        field_name="create_time", lookup_expr="lte",
        label="Date小于",
        widget=forms.DateTimeInput(attrs={'class': "form-control input-sm", 'placeholder': 'YYYY-MM-DD hh:mm'}))
    create_time__gte = django_filters.DateTimeFilter(
        field_name="create_time",
        lookup_expr="gte",
        label="Date大于",
        widget=forms.DateTimeInput(attrs={'class': "form-control input-sm", 'placeholder': 'YYYY-MM-DD hh:mm'}))

    class Meta:
        model = TimedTask
        fields = ["name", "host", "create_time__gte", "create_time__lte"]


class LogFilter(django_filters.FilterSet):
    cron_name = django_filters.CharFilter(
        field_name="cron_name", lookup_expr="icontains", label="任务名",
        widget=forms.TextInput(attrs={'class': "form-control input-sm"}))
    cron_server = django_filters.CharFilter(
        field_name="cron_server", lookup_expr="icontains", label="IP",
        widget=forms.TextInput(attrs={'class': "form-control input-sm"}))

    create_time__lte = django_filters.DateTimeFilter(
        field_name="create_time", lookup_expr="lte",
        label="Date小于",
        widget=forms.DateTimeInput(attrs={'class': "form-control input-sm", 'placeholder': 'YYYY-MM-DD hh:mm'}))
    create_time__gte = django_filters.DateTimeFilter(
        field_name="create_time",
        lookup_expr="gte",
        label="Date大于",
        widget=forms.DateTimeInput(attrs={'class': "form-control input-sm", 'placeholder': 'YYYY-MM-DD hh:mm'}))

    class Meta:
        model = TimedTask
        fields = ["cron_name", "cron_server", "create_time__gte", "create_time__lte"]
