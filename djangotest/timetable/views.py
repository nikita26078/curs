# Create your views here.
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView

from .models import Homework, Replacement
from .forms import LoginForm, UserRegistrationForm, ParamsForm, HomeworkForm, ReplacementForm
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


def user_logout(request):
    logout(request)
    return redirect("/")


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

            group = form.cleaned_data['group']
            request.session['group'] = group
            show_teacher = form.cleaned_data['show_teacher']
            request.session['show_teacher'] = show_teacher
            dictionary = {'days': get_timetable(group), 'show_teacher': show_teacher,
                          'current': get_current(), 'form': form}
            return redirect("/", context=dictionary)
        else:
            print(form.errors)
            error = 'Ошибка валидации'

    group = request.session.get('group')
    if group is None:
        group = '24'
        request.session['group'] = group

    show_teacher = request.session.get('show_teacher', False)

    dictionary = {'days': get_timetable(group), 'show_teacher': show_teacher,
                  'current': get_current(), 'form': form, 'error': error}
    return render(request, "timetable/index.html", context=dictionary)


def homework(request):
    return render(request, 'timetable/homework/main.html')


def replacements(request):
    replacement = Replacement.objects.filter(group=24).first()
    if request.method == 'POST':
        replacement_form = ReplacementForm(request.POST, request.FILES)
        if replacement_form.is_valid():
            replacement = replacement_form.save()
            return render(request, 'timetable/replacements.html',
                          {'replacement_form': replacement_form, 'replacement': replacement})
    else:
        group = request.session.get('group')
        if group is None:
            group = '24'
            request.session['group'] = group

        replacement_form = ReplacementForm(initial={'group': int(group)})
    return render(request, 'timetable/replacements.html',
                  {'replacement_form': replacement_form, 'replacement': replacement})


def homework_delete(request, id):
    obj = Homework.objects.get(id=id)
    obj.delete()
    mydictionary = {
        "object_list": Homework.objects.all()
    }
    return redirect("/homework/list", context=mydictionary)


def replacements_delete(request, id):
    obj = Replacement.objects.get(group=id)
    obj.delete()
    return replacements(request)


class HomeworkListView(ListView):
    model = Homework
    template_name = 'timetable/homework/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = Homework.objects.filter(user=self.request.user.id)
        return context


class HomeworkCreateView(CreateView):
    template_name = 'timetable/homework/add.html'
    form_class = HomeworkForm
    success_url = reverse_lazy('homework')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(HomeworkCreateView, self).form_valid(form)
