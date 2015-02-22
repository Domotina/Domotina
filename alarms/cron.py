# app/cron.py

import kronos
from random import randint
from django.contrib.auth.models import User

@kronos.register('* * * * *')
def check_alarms():
    list = User.objects.all();
    for user in list:
        print user
