import django_filters
from .models import Assets, SystemUser, PushSystemUserLog
from django import forms


class AssetsFilter(django_filters.FilterSet):
    ip = django_filters.CharFilter(
        field_name="ip", lookup_expr="icontains", label="IP匹配",
        widget=forms.TextInput(attrs={'class': "form-control input-sm"}))
    create_time__lte = django_filters.DateTimeFilter(
        field_name="create_time", lookup_expr="lte",
        label="Date小于",
        widget=forms.DateTimeInput(
            attrs={'class': "form-control input-sm", "id": "lt-date", 'placeholder': 'YYYY-MM-DD hh:mm'}))
    create_time__gte = django_filters.DateTimeFilter(
        field_name="create_time",
        lookup_expr="gte",
        label="Date大于",
        widget=forms.DateTimeInput(
            attrs={'class': "form-control input-sm", "id": "gt-date", 'placeholder': 'YYYY-MM-DD hh:mm'}))

    class Meta:
        model = Assets
        fields = ["ip", "create_time__gte", "create_time__lte"]


class PushUserFilter(django_filters.FilterSet):
    push_time__lte = django_filters.DateTimeFilter(
        field_name="push_time", lookup_expr="lte",
        label="Date小于",
        widget=forms.DateTimeInput(attrs={'class': "form-control input-sm", 'placeholder': 'YYYY-MM-DD hh:mm'}))

    push_time__gte = django_filters.DateTimeFilter(
        field_name="push_time", lookup_expr="gte",
        label="Date小于",
        widget=forms.DateTimeInput(attrs={'class': "form-control input-sm", 'placeholder': 'YYYY-MM-DD hh:mm'}))

    class Meta:
        model = PushSystemUserLog
        fields = ["push_time__lte", "push_time__gte"]
