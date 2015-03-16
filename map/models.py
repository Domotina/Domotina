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
        return self.name


class Place(models.Model):
    owner = models.ForeignKey(User, verbose_name="owner", related_name="places")
    neighborhood = models.ForeignKey(Neighborhood, verbose_name="neighborhood", related_name="places")
    name = models.CharField("place", max_length=100)
    #map = models.ImageField("map image", upload_to=settings.MAP_FILE_PATH)
    map = models.CharField("map image", max_length=255)
    date_created = models.DateTimeField("date created", auto_now_add=True)
    date_updated = models.DateTimeField("date updated", auto_now_add=True)

    class Meta:
        verbose_name = "place"
        verbose_name_plural = "places"
        ordering = ["neighborhood", "name"]

    def __unicode__(self):
        return self.name


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
        return self.name


class SensorType(models.Model):
    name = models.CharField("type", max_length=50)
    is_enabled = models.BooleanField("enabled?", default=True)
    is_continuous = models.BooleanField("continuous", default=False)

    class Meta:
        db_table = 'map_sensor_type'
        verbose_name = "sensor type"
        verbose_name_plural = "sensor types"
        ordering = ["name"]

    def __unicode__(self):
        return self.name


class SensorStatus(models.Model):
    type = models.ForeignKey(SensorType)
    name = models.CharField("status", max_length=50)
    icon = models.CharField("icon", max_length=255)
    is_enabled = models.BooleanField("enabled?", default=True)
    ref_code = models.IntegerField('ref code', default=0, blank=True, null=True)
    max_continuous = models.FloatField("max continuous", blank=True, null=True)
    min_continuous = models.FloatField("min continuous", blank=True, null=True)

    class Meta:
        db_table = 'map_sensor_status'
        verbose_name = "sensor status"
        verbose_name_plural = "sensor status"
        ordering = ["type", "name"]

    def __unicode__(self):
        return "%s: %s" % (self.type.name, self.name)


class Sensor(models.Model):
    asset = models.ForeignKey(Asset, verbose_name="asset", related_name="sensors")
    type = models.ForeignKey(SensorType, verbose_name="type", related_name="sensors")
    description = models.TextField("description", blank=True, null=True)
    date_created = models.DateTimeField("date created", auto_now_add=True)
    date_updated = models.DateTimeField("date updated", auto_now=True)
    # This columns are saved by event_manager
    current_status_id = models.PositiveIntegerField("current status id", default=0)
    current_pos_x = models.PositiveIntegerField("current X position in map", default=1)
    current_pos_y = models.PositiveIntegerField("current Y position in map", default=1)
    current_date = models.DateTimeField("current date")

    class Meta:
        verbose_name = "sensor"
        verbose_name_plural = "sensors"
        ordering = ["asset"]

    def __unicode__(self):
        return "Sensor on %s" % self.asset