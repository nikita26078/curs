from django.db import models


# Create your models here.

class Lesson:
    lesson: str
    group: str
    teacher_one: str
    cabinet_one: str
    teacher_two: str
    cabinet_two: str

    def __init__(self, lesson: str, group: str, teacher_one: str, cabinet_one: str, teacher_two: str,
                 cabinet_two: str):
        self.lesson = lesson
        self.group = group
        self.teacher_one = teacher_one
        self.cabinet_one = cabinet_one
        self.teacher_two = teacher_two
        self.cabinet_two = cabinet_two


class Day:
    lesson0: Lesson
    lesson1: Lesson
    lesson2: Lesson
    lesson3: Lesson
    lesson4: Lesson
    lesson5: Lesson
    lesson6: Lesson
    lesson7: Lesson
    week: str
    day: str

    def __init__(self, lesson0: Lesson, lesson1: Lesson, lesson2: Lesson, lesson3: Lesson, lesson4: Lesson,
                 lesson5: Lesson, lesson6: Lesson, lesson7: Lesson, week: str, day: str):
        self.lesson0 = lesson0
        self.lesson1 = lesson1
        self.lesson2 = lesson2
        self.lesson3 = lesson3
        self.lesson4 = lesson4
        self.lesson5 = lesson5
        self.lesson6 = lesson6
        self.lesson7 = lesson7
        self.week = week
        self.day = day


class Result:
    day: Day

    def __init__(self, day: Day):
        self.result = day
