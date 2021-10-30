# Create your views here.
from django.contrib.auth import login, authenticate
from django.shortcuts import render
from django.views.generic import TemplateView

from .forms import LoginForm, UserRegistrationForm
from .utils import process_timetable, get_timetable, get_current


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


class IndexListView(TemplateView):
    template_name = 'timetable/index.html'

    def get_context_data(self, **kwargs):
        result_holder = get_timetable()
        days = process_timetable(result_holder)

        context = super(IndexListView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['days'] = days
        context['current'] = get_current()
        return context
