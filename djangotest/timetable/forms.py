from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import ModelForm, CharField, PasswordInput, Form, ChoiceField

from .models import Homework


class UserRegistrationForm(ModelForm):
    password = CharField(label='Пароль', widget=PasswordInput)
    password2 = CharField(label='Повторите пароль', widget=PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise ValidationError('Пароли не совпадают.')
        return cd['password2']


class LoginForm(Form):
    username = CharField(label='Имя пользователя')
    password = CharField(label='Пароль', widget=PasswordInput)


class ParamsForm(Form):
    group = ChoiceField(label="Группа")


class HomeworkForm(ModelForm):
    class Meta:
        model = Homework
        fields = ['title', 'desc']
