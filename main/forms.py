from django.forms import ModelForm, TextInput, Select

class SearchVacancyForm(ModelForm):
    class Meta:
        fields = ['positionOrCompany', 'region']
        widgets = {
            'positionOrCompany': TextInput(),
            'region': Select(choices={
                'dp': 'Дніпро'
            })
        }