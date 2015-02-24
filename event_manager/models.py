from django.db import models
from sensor.models import Sensor

# Create your models here.

class EventType(models.Model):
    name = models.CharField('type', max_length=50)
    description = models.CharField('description', max_length=400)
    is_critical = models.BooleanField('is critical', default=False)

    class Meta:
        verbose_name = 'event type'
        verbose_name_plural = 'event types'

    def __unicode__(self):
        return self.type


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
        return self.pk + ' ' + self.sensor
