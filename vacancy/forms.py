from django.forms import ModelForm, Select, EmailInput, TextInput, Form
from tinymce.widgets import TinyMCE
from dal import autocomplete

from main.forms import MainSearchForm
from vacancy.models import Vacancy

class VacancySearchForm(MainSearchForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.update_placeholder('position', 'Посада або компанія')

class VacancyForm(ModelForm):
    class Meta:
        model = Vacancy
        fields = ['position', 'description', 'email', 'salary', 'phone_number', 'skills', 'employment_type']
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
            'skills': autocomplete.ModelSelect2Multiple(
                attrs={
                    'data-theme': 'bootstrap-5',
                    'data-placeholder': 'Навички',
                },
                url='main:jobskill-autocomplete'
            ),
        }