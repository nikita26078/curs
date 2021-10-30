# Create your views here.

from django.shortcuts import render
from django.views.generic import TemplateView

from .utils import process_timetable, get_timetable, get_current


def about(request):
    return render(request, 'timetable/about.html')


def contact(request):
    return render(request, 'timetable/contact.html')


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
