from django import forms
from .models import Resume, Job


class ResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ['name', 'resume']


class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = [
            'title',
            'company',
            'location',
            'salary',
            'description',
            'skills'
        ]