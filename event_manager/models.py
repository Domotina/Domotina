import threading
import traceback
from datetime import time, datetime

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from map.models import Sensor
from event_manager.notificator import send_email


def datetime_to_js(dt):
    return "new Date(%(year)s, %(month)s, %(day)s, %(h)s, %(m)s, %(s)s)" \
           % {'year': dt.strftime("%Y"),
              'month': dt.strftime("%m"),
              'day': dt.strftime("%d"),
              'h': dt.strftime("%H"),
              'm': dt.strftime("%M"),
              's': dt.strftime("%S")}


class Event(models.Model):
    sensor = models.ForeignKey(Sensor)
    timestamp = models.DateTimeField('date', auto_now_add=True)
    pos_x = models.IntegerField('x position', blank=True, null=True)
    pos_y = models.IntegerField('y position', blank=True, null=True)
    value = models.IntegerField('status', blank=True, null=True)

    class Meta:
        verbose_name = 'event'
        verbose_name_plural = 'events'

    def __unicode__(self):
        return "%s" % self.get_status()

    def is_reportable(self):
        # Create a flat to check if the event has to notify.
        notify = False
        # Search the sensor status of the event
        status = self.get_status()
        schedules = None
        # Search all daily schedule with status and sensor of the event
        if status:
            schedules = self.sensor.schedules.filter(status=status)
        '''
        If sensor has schedules to check, then check if any has broken
        a rule defined by the owner or domotina's central
        '''
        if schedules:
            for schedule in schedules:
                '''
                If sensor status on the event is between time intervals
                that is not allowed to using, then generate a alarm
                '''
                if (self.timestamp.time() > schedule.begin_time) and (self.timestamp.time() < schedule.end_time):
                    notify = True
                    break
        return notify

    def get_status(self):
        sensor = self.sensor
        if self.value is not None:
            sensor.current_value = self.value
            return sensor.get_status()
        else:
            return None

    def to_json(self):
        status = self.get_status()
        if status is None:
            return ''
        current_sensor = '{status: "%s", ' \
                         'url: "%s", ' \
                         'pos_x: %d, ' \
                         'pos_y: %d, ' \
                         'description: "%s", ' \
                         'sensor: %d, ' \
                         'timestamp: %s}' \
                         % (status.name,
                            status.icon,
                            self.pos_x,
                            self.pos_y,
                            self,
                            self.sensor.pk,
                            datetime_to_js(self.timestamp))
        return current_sensor


class Alarm(models.Model):
    event = models.ForeignKey(Event)
    notified = models.BooleanField('Is notified?', default=False)

    class Meta:
        verbose_name = 'alarm'
        verbose_name_plural = 'alarms'

    def __unicode__(self):
        return self.event


@receiver(post_save, sender=Event)
def event_handler(sender, instance, **kwargs):
    if instance.is_reportable():
        alarm = Alarm(event=instance)
        alarm.save()


@receiver(post_save, sender=Alarm)
def alarm_handler(sender, instance, created, **kwargs):
    if created:
        # Create a email with alarm
        d = threading.Thread(name='daemon', target=send_email(instance))
        d.setDaemon(True)
        try:
            d.start()
        except:
            print ("Error in check_schedule.")
            print traceback.format_exc()
            d.join()
        instance.notified = True
        instance.save()


@receiver(post_save, sender=Sensor)
def sensor_handler(sender, instance, created, **kwargs):
    event = Event(sensor=instance, value=instance.current_value, pos_x=instance.current_pos_x,
                  pos_y=instance.current_pos_y)
    event.save()
