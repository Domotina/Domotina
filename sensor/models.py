from django.db import models
from map.models import Place
from assets.models import Asset

# Create your models here.
class SensorStatus(models.Model):
    name = models.CharField('type',max_length=20)
    class Meta:
        verbose_name = 'sensor_status'
        verbose_name_plural = 'sensor_status'

    def __unicode__(self):
        return self.name

class SensorType(models.Model):
    type = models.CharField('type of sensor', max_length=50)
    class Meta:
        verbose_name = 'sensor_type'
        verbose_name_plural = 'sensor_types'

    def __unicode__(self):
        return self.type

class Sensor(models.Model):
    place = models.ForeignKey(Place)
    type = models.ForeignKey(SensorType)
    description = models.TextField('description')
    status = models.ForeignKey(SensorStatus)
    asset = models.ForeignKey(Asset,related_name='asset',null=True, blank=True)
    coord_x = models.PositiveIntegerField('coord X in map', blank=True, null=True)
    coord_y = models.PositiveIntegerField('coord Y in map', blank=True, null=True)

    class Meta:
        verbose_name = 'sensor'
        verbose_name_plural = 'sensors'

    def __unicode__(self):
        return self.pk + " - " + self.type