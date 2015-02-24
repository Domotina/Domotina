from django.db import models
from event_manager.models import Event

class Alarm(models.Model):
    event = models.ForeignKey(Event)
    activation_date = models.DateTimeField('activation date', auto_now_add=True)
    activated = models.BooleanField('Is activated?', default=True)
    notified = models.BooleanField('Is notified?', default=False)

    class Meta:
        verbose_name = 'alarm'
        verbose_name_plural = 'alarms'

    def __unicode__(self):
        return self.pk + ' - Event: ' + self.event
