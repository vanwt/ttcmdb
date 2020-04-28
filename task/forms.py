from django import forms
from .models import AnsiblePlaybook


class CreatePlaybook(forms.ModelForm):
    playbook_name = forms.CharField(
        label="剧本名",
        max_length=32,
        widget=forms.TextInput(
            attrs={"class": "form-control"}
        )
    )
    playbook_file = forms.FileField(
        label="上传剧本",
        required=False
    )
    playbook_content = forms.CharField(
        label="剧本内容",
        required=False,
        help_text="剧本内容与上传剧本二选一,若两个同时选择，优先使用上传的PlayBook",
        widget=forms.Textarea(
            attrs={"class": "form-control"}
        )
    )
    playbook_desc = forms.CharField(
        label="剧本描述",
        required=False,
        widget=forms.Textarea(
            attrs={"class": "form-control", "cols": "40", "rows": "5", }
        )
    )

    class Meta:
        model = AnsiblePlaybook
        fields = ["playbook_name", "playbook_file", "playbook_content", "playbook_desc"]
