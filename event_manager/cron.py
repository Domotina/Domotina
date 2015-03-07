# app/cron.py

import kronos

from event_manager import notificator
from event_manager.models import Alarm


@kronos.register('* * * * *')
def check_alarms():
    current_alarms = Alarm.objects.get(activated=True)
    for alarm in current_alarms:
        notificator.send_email(alarm)

