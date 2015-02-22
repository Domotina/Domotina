from django.db import models

# Create your models here.

class EventType(models.Model):
    name = models.CharField('type', max_length=50)
    is_critical = models.BooleanField('is critical')

    class Meta:
        verbose_name = 'type_event'
        verbose_name_plural = 'type_events'

    def __unicode__(self):
        return self.type


class Event(models.Model):
#    sensor = models.ForeignKey(Sensor)
    type = models.ForeignKey(EventType)
    timestamp = models.DateTimeField('date', auto_now_add=True)

    class Meta:
        verbose_name = 'event'
        verbose_name_plural = 'events'

    def __unicode__(self):
        return self.pk + ' ' + self.sensor
