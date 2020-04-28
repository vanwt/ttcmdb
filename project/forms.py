from django import forms
from .models import Project
from user.models import User
from assets.models import Assets


class CreateProjectForm(forms.ModelForm):
    project_name = forms.CharField(
        label='项目名',
        widget=forms.TextInput(
            attrs={"class": "form-control"}
        )
    )
    project_desc = forms.CharField(
        label='项目说明',
        required=False,
        widget=forms.Textarea(
            attrs={"class": "form-control", "cols": 40, "rows": 5}
        )
    )
    auth_users = forms.ModelMultipleChoiceField(
        label='授权用户',
        required=False,
        queryset=User.get_all(),
        widget=forms.SelectMultiple(
            attrs={"class": "form-control selectpicker", "data-live-search": "true", "data-size": "5",
                   "data-width": "100%", }
        )
    )
    assets_set = forms.ModelMultipleChoiceField(
        label="旗下资产",
        required=False,
        help_text="如果你从资产创建打开此页面，晴忽略该项内容",
        queryset=Assets.get_all(),
        widget=forms.SelectMultiple(
            attrs={
                "class": "selectpicker", "data-live-search": "true", "data-size": "5",
                "data-width": "100%",
            }
        )
    )

    class Meta:
        model = Project
        fields = ['project_name', 'project_desc', 'auth_users', 'assets_set']

    def clean_project_name(self):
        pro_name = self.cleaned_data['project_name']
        name = Project.get_by_name(pro_name)
        if name:
            raise forms.ValidationError("该项目已存在")
        return pro_name


class UpdateProjectForm(forms.ModelForm):
    project_name = forms.CharField(
        label='项目名',
        widget=forms.TextInput(
            attrs={"class": "form-control"}
        )
    )
    project_desc = forms.CharField(
        label='项目说明',
        required=False,
        widget=forms.Textarea(
            attrs={"class": "form-control", "cols": 40, "rows": 5}
        )
    )
    auth_users = forms.ModelMultipleChoiceField(
        label='授权用户',
        required=False,
        queryset=User.get_all(),
        widget=forms.SelectMultiple(
            attrs={"class": "form-control selectpicker", "data-live-search": "true", "data-size": "5",
                   "data-width": "100%", }
        )
    )
    assets_set = forms.ModelMultipleChoiceField(
        label="旗下资产",
        required=False,
        help_text="如果你从资产创建打开此页面，晴忽略该项内容",
        queryset=Assets.get_all(),
        widget=forms.SelectMultiple(
            attrs={
                "class": "selectpicker", "data-live-search": "true", "data-size": "5",
                "data-width": "100%",
            }
        )
    )

    class Meta:
        model = Project
        fields = ['project_name', 'project_desc', 'auth_users', 'assets_set']
