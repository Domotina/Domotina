# app/cron.py

import kronos
from django.contrib.auth.models import User
from alarms.models import Alarm
from alarms import notificator

@kronos.register('* * * * *')
def check_alarms():
    current_alarms = Alarm.objects.get(activated=True)
    for alarm in current_alarms:
        notificator.send_email(alarm)

