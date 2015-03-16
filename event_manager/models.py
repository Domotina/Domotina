from django.db import models
from map.models import Sensor
from django.db.models.signals import post_save
from django.dispatch import receiver
from notificator import send_email

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
    status = models.IntegerField('status', blank=True, null=True)
    value = models.FloatField('value (for continuous)', blank=True, null=True)

    class Meta:
        verbose_name = 'event'
        verbose_name_plural = 'events'

    def __unicode__(self):
        return "%s at %s" % (self.type, self.timestamp)


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
    if instance.status is not None:
        instance.sensor.current_status_id = instance.status
    if instance.pos_x is not None:
        instance.sensor.current_pos_x = instance.pos_x
    if instance.pos_y is not None:
        instance.sensor.current_pos_y = instance.pos_y
    instance.sensor.current_date = instance.timestamp
    instance.sensor.save()


@receiver(post_save, sender=Alarm)
def alarmHandler(sender, instance, created, **kwargs):
    if(created):
        send_email(instance)
        instance.notified = True
        instance.activated = False
        instance.save()