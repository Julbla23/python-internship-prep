from django import forms
from django.forms import ModelForm


from .models import PRIORITY_CHOICES, STATUS_CHOICES, Task, Category


class AddTask(forms.Form):
    title = forms.CharField(max_length=50)
    planned_date = forms.DateTimeField(
        widget=forms.DateTimeInput(
            attrs={'type': 'datetime-local'}
        )
    )
    deadline = forms.DateField(
        widget=forms.DateInput(
            attrs={'type':'date'}
        ), required=False
    )
    duration_minutes = forms.IntegerField(required=True)
    priority = forms.ChoiceField(choices=PRIORITY_CHOICES)
    status = forms.ChoiceField(choices=STATUS_CHOICES)
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=False)

class EditTask(ModelForm):
    class Meta:
        model = Task
        fields = [
            "name",
            "planned_date",
            "deadline",
            "duration_minutes",
            "priority",
            "status",
            "category",
        ]

