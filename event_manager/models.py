from django.db import models
from map.models import Sensor, SensorStatus, SensorType
from django.db.models.signals import post_save
from django.dispatch import receiver
from map.models import SensorStatus
from rule_engine.models import ScheduleDaily
from event_manager.notificator import send_email
import threading
import traceback

# Create your models here.


class EventType(models.Model):
    name = models.CharField('name', max_length=50)
    description = models.CharField('description', max_length=400)
    is_critical = models.BooleanField('is critical', default=False)

    class Meta:
        verbose_name = 'event type'
        verbose_name_plural = 'event types'

    def __unicode__(self):
        return self.name


class Event(models.Model):
    sensor = models.ForeignKey(Sensor)
    type = models.ForeignKey(EventType)
    timestamp = models.DateTimeField('date', auto_now_add=True)
    pos_x = models.IntegerField('x position', blank=True, null=True)
    pos_y = models.IntegerField('y position', blank=True, null=True)
    value = models.IntegerField('status', blank=True, null=True)

    class Meta:
        verbose_name = 'event'
        verbose_name_plural = 'events'

    def __unicode__(self):
        return "%s at %s" % (self.type, self.timestamp)

    def is_reportable(self):
        # Create a flat to check if the event has to notify.
        notify = False;
        # Search the sensor status of the event
        status = SensorStatus.objects.filter(value=self.value,type=self.sensor.type)[0]
        # Search all daily schedule with status and sensor of the event
        schedules = ScheduleDaily.objects.filter(status=status, sensor=self.sensor)
        # If sensor has schedules to check, then check if any has broken a rule defined by the owner or domotina's central.
        if schedules:
            for schedule in schedules:
                # If sensor status on the event is between time intervals that is not allowed to using, then generate a alarm.
                if (self.timestamp.time() > schedule.begin_time) & (self.timestamp.time() < schedule.end_time):
                   # Check the type of action to take on schedule
                   if schedule.actionType.id == 1:
                       notify = True
                       print ("A schedule was checked and processed")
                else:
                    print ("The sensor is OK with the rule: "+ str(schedule))

        else:
            print ("The sensor self does not have schedules.")
        return notify

class Alarm(models.Model):
    event = models.ForeignKey(Event)
    activation_date = models.DateTimeField('activation date', auto_now_add=True)
    activated = models.BooleanField('Is activated?', default=True)
    notified = models.BooleanField('Is notified?', default=False)

    class Meta:
        verbose_name = 'alarm'
        verbose_name_plural = 'alarms'

    def __unicode__(self):
        return "Alarm from %s" % self.event


@receiver(post_save, sender=Event)
def myHandler(sender, instance, **kwargs):
    if instance.type.is_critical:
        alarm = Alarm(event=instance)
        alarm.save()
    if instance.value is not None:
        instance.sensor.current_value = instance.value
    if instance.pos_x is not None:
        instance.sensor.current_pos_x = instance.pos_x
    if instance.pos_y is not None:
        instance.sensor.current_pos_y = instance.pos_y
    instance.sensor.current_date = instance.timestamp
    instance.sensor.save()


@receiver(post_save, sender=Alarm)
def alarmHandler(sender, instance, created, **kwargs):
    if(created):
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
        instance.activated = False
        instance.save()