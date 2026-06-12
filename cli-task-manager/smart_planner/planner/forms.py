from django import forms
from isort.profiles import attrs

from .models import PRIORITY_CHOICES, STATUS_CHOICES

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