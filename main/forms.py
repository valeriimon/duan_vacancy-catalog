from django.forms import Form, TextInput, Select, CharField, ChoiceField

from user.models import REGIONS


class MainSearchForm(Form):
    position = CharField(
        required=False,
        widget=TextInput(attrs={
            'class': 'form-control position-control',
            'placeholder': 'Посада',
        })
    )
    region = ChoiceField(
        choices=REGIONS,
        widget=Select(
            attrs={
                'class': 'form-control region-control',
                'placeholder': 'Регіон'
            },
        )
    )

    def update_placeholder(self, field_name, value):
        self.fields[field_name].widget.attrs.update({
            'placeholder': value,
        })

