from django.urls import path

from . import views
from .views import *

urlpatterns = [
    path('', views.view, name='index'),
    path('about', views.about, name='about'),
    path('contact', views.contact, name='contact'),
    path('register', views.register, name='register'),
    path('login', views.user_login, name='login'),
    path('profile', views.profile, name='profile'),
    path('view', views.view, name='view'),
    path('homework', views.homework, name='homework'),
    path('homework/list', HomeworkListView.as_view(), name='homework_list'),
    path('homework/add', HomeworkCreateView.as_view(), name='homework_add'),
    path('homework/delete/<int:id>', views.homework_delete, name='homework_delete'),
    path('replacements', views.replacements, name='replacements'),
    path('replacements/delete/<int:id>', views.replacements_delete, name='replacements_delete'),
]
