from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import ModelForm, CharField, PasswordInput, Form, ChoiceField, BooleanField
from django.forms.widgets import HiddenInput

from .models import Homework, Replacement


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
    show_teacher = BooleanField(label="Показывать преподавателей", required=False)
    group = ChoiceField(label="Группа")


class TeacherForm(Form):
    teacher = ChoiceField(label="Преподаватель")


class HomeworkForm(ModelForm):
    class Meta:
        model = Homework
        fields = ['title', 'desc', 'subj', 'user']
        widgets = {
            'user': HiddenInput(),
        }


class ReplacementForm(ModelForm):
    class Meta:
        model = Replacement
        fields = ['img', 'group']
        widgets = {
            'group': HiddenInput(),
        }
