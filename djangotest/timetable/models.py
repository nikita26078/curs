from django.contrib.auth.models import User
from django.db import models


class Homework(models.Model):
    title = models.CharField('Название', max_length=255)
    subj = models.CharField('Предмет', max_length=255)
    desc = models.TextField('Описание', default='', blank=True)
    user = models.ForeignKey(User, related_name='shipper', on_delete=models.CASCADE,
                             default=None, null=True, blank=True, verbose_name='Пользователь')


class Replacement(models.Model):
    img = models.ImageField('Изображение', upload_to='images/')
    group = models.IntegerField('Группа', primary_key=True)
