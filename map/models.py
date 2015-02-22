from django.conf import settings
from django.db import models
from django.contrib.auth.models import User

class Building(models.Model):
    name = models.CharField('building', max_length=100)
    class Meta:
        verbose_name = 'building'
        verbose_name_plural = 'buildings'
        ordering = ['name']

    def __unicode__(self):
        return '%s' % self.name

class Place(models.Model):
    owner = models.ForeignKey(User)
    building = models.ForeignKey(Building, verbose_name="building", related_name="places")
    name = models.CharField('place', max_length=100)
    map = models.ImageField('map image', upload_to=settings.UPLOADED_MAP_FILE_PATH)
    class Meta:
        verbose_name = 'place'
        verbose_name_plural = 'places'
        ordering = ['name']

    def __unicode__(self):
        return '%s %s' % (self.building.name, self.name)


class Door(models.Model):
    place = models.ForeignKey(Place, verbose_name="place", related_name="doors")
    name = models.CharField('door', max_length=100)
    coord_x = models.PositiveIntegerField('coord X in map', blank=True, null=True)
    coord_y = models.PositiveIntegerField('coord Y in map', blank=True, null=True)
    is_locked = models.BooleanField('locked?', default=True)
    class Meta:
        verbose_name = 'door'
        verbose_name_plural = 'doors'
        ordering = ['name']

    def __unicode__(self):
        return '%s: %s(%s,%s)' % (self.place, self.name, self.coord_x, self.coord_y)

class Window(models.Model):
    place = models.ForeignKey(Place, verbose_name="place", related_name="windows")
    name = models.CharField('door', max_length=100)
    coord_x = models.PositiveIntegerField('coord X in map', blank=True, null=True)
    coord_y = models.PositiveIntegerField('coord Y in map', blank=True, null=True)
    is_locked = models.BooleanField('locked?', default=True)
    class Meta:
        verbose_name = 'window'
        verbose_name_plural = 'windows'
        ordering = ['name']

    def __unicode__(self):
        return '%s: %s(%s,%s)' % (self.place, self.name, self.coord_x, self.coord_y)

class Device(models.Model):
    place = models.ForeignKey(Place, verbose_name = "place", related_name = "devices")
    name = models.CharField('device', max_length=100)
    coord_x = models.PositiveIntegerField('coord X in model', blank=True, null=True)
    coord_y = models.PositiveIntegerField('coord Y in model', blank=True, null=True)
    is_locked = models.BooleanField('locked?', default=True)
    class Meta:
        verbose_name = 'device'
        verbose_name_plural = 'devices'
        ordering = ['name']

    def __unicode__(self):
        return '%s' % self.name