import django_filters
from .models import Project
from django import forms


class ProjectFilter(django_filters.FilterSet):
    project_name = django_filters.CharFilter(
        field_name="project_name", lookup_expr="icontains", label="项目名",
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
        model = Project
        fields = ["project_name", "create_time__gte", "create_time__lte"]
