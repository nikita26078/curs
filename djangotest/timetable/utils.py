import datetime
import json

import requests
from urllib3.exceptions import InsecureRequestWarning

from django.conf import settings

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

weekdays = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница']


def process_timetable(result):
    days = {}
    i = 0
    for day in result:
        tag_day = str(i)
        days[tag_day] = {}
        days[tag_day]['name'] = weekdays[i]
        days[tag_day]['lessons'] = {}
        for lesson in day['result']:
            if lesson.isdigit() and lesson != 'name':
                days[tag_day]['lessons'][lesson] = day['result'][lesson]
        i += 1
    return days


def get_timetable(group):
    if settings.DEBUG:
        with open('data.json', 'r') as f:
            json_data = json.load(f)
    else:
        json_data = requests.get('https://rasp.source-point.ru/timetable/rasp?gid=' + group, verify=False).json()
    return process_timetable(json_data)


def get_current():
    current = {}
    time_now = datetime.datetime.now()
    day_now = time_now.weekday()
    day = day_now if day_now < 5 else 0
    current['day'] = str(day)
    hour_now = time_now.time()
    lesson = -1
    if hour_now >= datetime.time(16, 25):
        lesson = -1
    elif hour_now >= datetime.time(15, 40):
        lesson = 7
    elif hour_now >= datetime.time(14, 45):
        lesson = 6
    elif hour_now >= datetime.time(13, 50):
        lesson = 5
    elif hour_now >= datetime.time(12, 50):
        lesson = 4
    elif hour_now >= datetime.time(11, 50):
        lesson = 3
    elif hour_now >= datetime.time(10, 50):
        lesson = 2
    elif hour_now >= datetime.time(9, 55):
        lesson = 1
    elif hour_now >= datetime.time(9, 0):
        lesson = 0
    current['lesson'] = str(lesson)
    return current


def get_groups():
    result = requests.get('https://rasp.source-point.ru/timetable/parameters', verify=False).json()
    groups = []
    for group in result['group']:
        groups.append((group['id_group'], group['number_group']))
    return groups
