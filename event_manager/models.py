from django.db import models
from map.models import Sensor
from actstream import registry, action
from django.db.models.signals import post_save
from django.dispatch import receiver

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
    pos_x = models.IntegerField('x position', default=0)
    pos_y = models.IntegerField('y position', default=0)

    class Meta:
        verbose_name = 'event'
        verbose_name_plural = 'events'

    def __unicode__(self):
        return "%(type) on %(timestamp)" % {'type': self.type, 'timestamp': self.timestamp}


class Alarm(models.Model):
    event = models.ForeignKey(Event)
    activation_date = models.DateTimeField('activation date', auto_now_add=True)
    activated = models.BooleanField('Is activated?', default=True)
    notified = models.BooleanField('Is notified?', default=False)

    class Meta:
        verbose_name = 'alarm'
        verbose_name_plural = 'alarms'

    def __unicode__(self):
        return "%(id) - Event: %(event)" % {'id': self.pk, 'event': self.event}


registry.register(Event)
registry.register(EventType)

@receiver(post_save, sender=Event)
def myHandler(sender, instance, **kwargs):
    action.send(instance.sensor, verb="reported", action_object=instance.type, target=instance.sensor.asset)