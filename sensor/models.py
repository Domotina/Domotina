from django.conf import settings
from django.db import models
from django.contrib.auth.models import User

class Neighborhood(models.Model):
    name = models.CharField("neighborhood", max_length=100)
    date_created = models.DateTimeField("date created", auto_now_add=True)
    date_updated = models.DateTimeField("date updated", auto_now_add=True)

    class Meta:
        verbose_name = "neighborhood"
        verbose_name_plural = "neighborhoods"
        ordering = ["name"]

    def __unicode__(self):
        return "%s" % self.name


class Place(models.Model):
    owner = models.ForeignKey(User, verbose_name="owner", related_name="places")
    neighborhood = models.ForeignKey(Neighborhood, verbose_name="neighborhood", related_name="places")
    name = models.CharField("place", max_length=100)
    map = models.ImageField("map image", upload_to=settings.SENSOR_MAP_FILE_PATH)
    date_created = models.DateTimeField("date created", auto_now_add=True)
    date_updated = models.DateTimeField("date updated", auto_now_add=True)

    class Meta:
        verbose_name = "place"
        verbose_name_plural = "places"
        ordering = ["neighborhood", "name"]

    def __unicode__(self):
        return "%s %s" % (self.neighborhood.name, self.name)


class Asset(models.Model):
    place = models.ForeignKey(Place, verbose_name="place", related_name="assets")
    name = models.CharField("asset", max_length=50)
    description = models.TextField("description", blank=True, null=True)
    date_created = models.DateTimeField("date created", auto_now_add=True)
    date_updated = models.DateTimeField("date updated", auto_now_add=True)

    class Meta:
        verbose_name = "asset"
        verbose_name_plural = "assets"
        ordering = ["place", "name"]

    def __unicode__(self):
        return "%s %s: %s" % (self.place.neighborhood.name, self.place.name, self.name)


class SensorType(models.Model):
    name = models.CharField("type", max_length=50)
    is_enabled = models.BooleanField("enabled?", default=True)

    class Meta:
        verbose_name = "sensor type"
        verbose_name_plural = "sensor types"
        ordering = ["name"]

    def __unicode__(self):
        return "%s" % (self.name)


class SensorStatus(models.Model):
    type = models.ForeignKey(SensorType)
    name = models.CharField("status", max_length=50)
    icon = models.ImageField("icon", upload_to=settings.SENSOR_ICONS_FILE_PATH)
    is_enabled = models.BooleanField("enabled?", default=True)

    class Meta:
        verbose_name = "sensor status"
        verbose_name_plural = "sensor status"
        ordering = ["type", "name"]

    def __unicode__(self):
        return "%s: %s" % (self.type.name, self.name)


class Sensor(models.Model):
    asset = models.ForeignKey(Asset, verbose_name="asset", related_name="sensors")
    status = models.ForeignKey(SensorStatus, verbose_name="status", related_name="sensors")
    pos_x = models.PositiveIntegerField("X position in map", default=1)
    pos_y = models.PositiveIntegerField("Y position in map", default=1)
    description = models.TextField("description", blank=True, null=True)
    date_created = models.DateTimeField("date created", auto_now_add=True)
    date_updated = models.DateTimeField("date updated", auto_now_add=True)

    class Meta:
        verbose_name = "sensor"
        verbose_name_plural = "sensors"
        ordering = ["asset"]

    def __unicode__(self):
        return "SENSOR MONITORING %s" % (self.asset.name)