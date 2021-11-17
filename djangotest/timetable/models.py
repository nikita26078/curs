from django.db import models


class Homework(models.Model):
    title = models.CharField('Название', max_length=255)
    desc = models.TextField('Описание')
