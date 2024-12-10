from tinymce.widgets import TinyMCE
from django.forms import ModelForm, Select, EmailInput, TextInput
from dal import autocomplete

from .models import Resume



class ResumeForm(ModelForm):
    class Meta:
        model = Resume
        fields = ['position', 'region', 'description', 'email', 'salary', 'phone_number', 'skills', 'employment_type']
        widgets = {
            'position': autocomplete.ModelSelect2(
                attrs={
                    'data-theme': 'bootstrap-5',
                    'data-placeholder': 'Позиція'
                },
                url='main:jobposition-autocomplete'
            ),
            'description': TinyMCE(attrs={
                'class': 'form-control mt-3'
            }),
            'employment_type': Select(attrs={
                'class': 'form-control'
            }),
            'salary': TextInput(attrs={
                'class': 'form-control'
            }),
            'email': EmailInput(attrs={
                'class': 'form-control',
            }),
            'phone_number': TextInput(attrs={
                'class': 'form-control',
            }),
            'region': Select(attrs={
                'class': 'form-control'
            }),
            'skills': autocomplete.ModelSelect2Multiple(
                attrs={
                    'create_id': 'true',
                    'data-theme': 'bootstrap-5',
                    'data-placeholder': 'Навички',
                },
                url='main:jobskill-autocomplete'
            ),
        }