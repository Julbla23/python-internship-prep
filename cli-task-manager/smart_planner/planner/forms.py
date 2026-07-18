from django import forms
from django.forms import ModelForm


from .models import PRIORITY_CHOICES, STATUS_CHOICES, Task

class AddTask(forms.Form):
    title = forms.CharField(max_length=50)
    planned_date = forms.DateField(
        widget=forms.DateInput(
            attrs={'type': 'date'}
        )
    )
    deadline = forms.DateField(
        widget=forms.DateInput(
            attrs={'type':'date'}
        ), required=False
    )
    duration_minutes = forms.IntegerField(min_value=1)
    priority = forms.ChoiceField(choices=PRIORITY_CHOICES)
    status = forms.ChoiceField(choices=STATUS_CHOICES)

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
        ]