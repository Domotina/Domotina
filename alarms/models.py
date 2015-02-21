from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.
class Status(models.Model):
    status = models.CharField('state', max_length=50)

    class Meta:
        verbose_name = 'state'
        verbose_name_plural = 'status'

    def __unicode__(self):
        return self.status


class Property(models.Model):
    owner = models.ForeignKey(User)
    address = models.CharField('address', max_length=100)
    phone = models.IntegerField('phone', max_length=10)
    description = models.TextField('description')
    registration_date = models.DateField('date of registration', auto_now_add=True)
    status = models.ForeignKey(Status)

    class Meta:
        verbose_name = 'property'
        verbose_name_plural = 'properties'

    def __unicode__(self):
        return self.address


class Map(models.Model):
    property_ref = models.ForeignKey(Property)
    map = models.ImageField('map', upload_to=settings.UPLOADED_FILE_PATH)
    creation = models.DateField('Date of creation', auto_now_add=True)

    class Meta:
        verbose_name = 'map'
        verbose_name_plural = 'maps'

    def __unicode__(self):
        return "Map: " + self.property_ref


class SensorType(models.Model):
    type = models.CharField('type of sensor', max_length=50)

    class Meta:
        verbose_name = 'sensor_type'
        verbose_name_plural = 'sensor_types'

    def __unicode__(self):
        return self.type


class Asset(models.Model):
    property = models.ForeignKey(Property)
    name = models.CharField('name', max_length=50)
    description = models.TextField('description')
    creation = models.DateField('date of registration', auto_now_add=True)
    status = models.ForeignKey(Status)

    class Meta:
        verbose_name = 'asset'
        verbose_name_plural = 'assets'

    def __unicode__(self):
        return self.name


class Sensor(models.Model):
    installed = models.ForeignKey(Property)
    type = models.ForeignKey(SensorType)
    description = models.TextField('description')
    asset = models.ForeignKey(Asset,related_name='asset',null=True, blank=True)
    status = models.ForeignKey(Status)

    class Meta:
        verbose_name = 'sensor'
        verbose_name_plural = 'sensors'

    def __unicode__(self):
        return self.pk + " - " + self.type


class TypeEvent(models.Model):
    type = models.CharField('type', max_length=50)

    class Meta:
        verbose_name = 'type_event'
        verbose_name_plural = 'type_events'

    def __unicode__(self):
        return self.type


class Event(models.Model):
    sensor = models.ForeignKey(Sensor)
    type = models.ForeignKey(TypeEvent)
    date = models.DateTimeField('date')

    class Meta:
        verbose_name = 'event'
        verbose_name_plural = 'events'

    def __unicode__(self):
        return self.pk + ' ' + self.sensor


class Alarm(models.Model):
    event = models.ForeignKey(Event)
    activation_date = models.DateTimeField('activation date', auto_now_add=True)
    activated = models.BooleanField('Is activated?', default=True)
    notified = models.BooleanField('Is notified?', default=False)
    status = models.ForeignKey(Status)

    class Meta:
        verbose_name = 'alarm'
        verbose_name_plural = 'alarms'

    def __unicode__(self):
        return self.pk + ' - Event: ' + self.event