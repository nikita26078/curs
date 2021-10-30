from django.urls import path

from . import views
from .views import *

urlpatterns = [
    path('', IndexListView.as_view(), name='index'),
    path('about', views.about, name='about'),
    path('contact', views.contact, name='contact'),
]
