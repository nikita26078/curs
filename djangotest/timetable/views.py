# Create your views here.
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView

from .models import Homework
from .forms import LoginForm, UserRegistrationForm, ParamsForm, HomeworkForm
from .utils import get_timetable, get_current, get_groups


def about(request):
    return render(request, 'timetable/about.html')


def contact(request):
    return render(request, 'timetable/contact.html')


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            return render(request, 'timetable/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'timetable/register.html', {'user_form': user_form})


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return render(request, 'timetable/login_done.html', {'new_user': user})
                else:
                    return render(request, 'timetable/login_failed.html', {'text': 'Аккаунт отключен'})
            else:
                return render(request, 'timetable/login_failed.html', {'text': 'Неверные данные'})
    else:
        form = LoginForm()
    return render(request, 'timetable/login.html', {'form': form})


def profile(request):
    if request.user.is_anonymous:
        return user_login(request)
    else:
        data = {
            'profile': request.user,
        }
        return render(request, 'timetable/profile.html', data)


def view(request):
    error = ''
    form = ParamsForm(request.POST or None, initial=request.session.get('form_data'))
    choices = request.session.get('choices')
    if choices is None:
        choices = get_groups()
        request.session['choices'] = choices
    form.fields['group'].choices = choices

    if request.method == 'POST':
        if form.is_valid():
            request.session['form_data'] = form.cleaned_data
            group = form.data['group']
            request.session['group'] = group
            dictionary = {'days': get_timetable(group), 'current': get_current(), 'form': form}
            return redirect("/", context=dictionary)
        else:
            print(form.errors)
            error = 'Ошибка валидации'

    group = request.session.get('group')
    if group is None:
        group = '24'
        request.session['group'] = group

    dictionary = {'days': get_timetable(group), 'current': get_current(), 'form': form, 'error': error}
    return render(request, "timetable/index.html", context=dictionary)


def homework(request):
    return render(request, 'timetable/homework/main.html')


def homework_delete(request, id):
    obj = Homework.objects.get(id=id)
    obj.delete()
    mydictionary = {
        "object_list": Homework.objects.all()
    }
    return redirect("/homework/list", context=mydictionary)


class HomeworkListView(ListView):
    model = Homework
    template_name = 'timetable/homework/list.html'


class HomeworkCreateView(CreateView):
    template_name = 'timetable/homework/add.html'
    form_class = HomeworkForm
    success_url = reverse_lazy('homework')
