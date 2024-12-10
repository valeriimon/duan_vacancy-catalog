
from django.forms import ModelForm, EmailInput, TextInput, PasswordInput, Select, NumberInput, Form, CharField
from user.models import User, Company


class SigninForm(Form):
    username = CharField(widget=TextInput(attrs={
                'class': 'form-control mb-3',
                'placeholder': "Ваше ім'я"
            }))

    password = CharField(widget=PasswordInput(attrs={
                'class': 'form-control mb-3',
                'placeholder': 'Пароль'
            }))


class SignupForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'age', 'email', 'password', 'region']
        widgets = {
            'username': TextInput(attrs={
                'class': 'form-control mb-3',
                'placeholder': "Ваше ім'я"
            }),
            'email': EmailInput(attrs={
                'class': 'form-control mb-3',
                'placeholder': 'Ел. пошта',
                'required': 'true'
            }),
            'password': PasswordInput(attrs={
                'class': 'form-control mb-3',
                'placeholder': 'Пароль',
                'required': 'true'
            }),
            'age': NumberInput(attrs={
                'class': 'form-select mb-3',
                'placeholder': 'Вік',
            }),
            'region': Select(attrs={
                'class': 'form-select mb-3',
                'required': 'true'
            })
        }

class CompanyForm(ModelForm):
    class Meta:
        model = Company
        fields = ['name', 'address_text', 'region', 'phone_number', 'employees_count']
        widgets = {
            'name': TextInput(attrs={
                'class': 'form-control mb-3',
                'placeholder': 'Назва компанії',
                'required': 'true'
            }),
            'address_text': TextInput(attrs={
                'class': 'form-control mb-3',
                'placeholder': 'Адреса',
            }),
            'region': Select(attrs={
                'class': 'form-select mb-3',
                'required': 'true'
            }),
            'phone_number': TextInput(attrs={
                'class': 'form-control mb-3',
                'placeholder': 'Телефон',
                'type': 'phone'
            }),
            'employees_count': NumberInput(attrs={
                'class': 'form-control mb-3',
                'placeholder': 'Кількість співробітників'
            })
        }