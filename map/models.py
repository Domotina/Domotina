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
    date_created = models.DateTimeField("date created", auto_now_add=True)
    date_updated = models.DateTimeField("date updated", auto_now_add=True)

    class Meta:
        verbose_name = "place"
        verbose_name_plural = "places"
        ordering = ["neighborhood", "name"]

    def __unicode__(self):
        return self.name


class Floor(models.Model):
    place = models.ForeignKey(Place, verbose_name="place", related_name="floors")
    number = models.PositiveIntegerField("number", default=1)
    #map = models.ImageField("map image", upload_to=settings.MAP_FILE_PATH)
    map = models.CharField("map image", max_length=255)
    date_created = models.DateTimeField("date created", auto_now_add=True)
    date_updated = models.DateTimeField("date updated", auto_now_add=True)

    class Meta:
        verbose_name = "floor"
        verbose_name_plural = "floors"
        ordering = ["place", "number"]

    def __unicode__(self):
        return "%s Floor %s" % (self.place, self.number)


'''class Asset(models.Model):
    floor = models.ForeignKey(Floor, verbose_name="floor", related_name="assets")
    name = models.CharField("asset", max_length=50)
    description = models.TextField("description", blank=True, null=True)
    date_created = models.DateTimeField("date created", auto_now_add=True)
    date_updated = models.DateTimeField("date updated", auto_now_add=True)

    class Meta:
        verbose_name = "asset"
        verbose_name_plural = "assets"
        ordering = ["floor", "name"]

    def __unicode__(self):
        return self.name'''


class SensorType(models.Model):
    name = models.CharField("type", max_length=50)
    is_enabled = models.BooleanField("is enabled", default=True)
    is_continuous = models.BooleanField("continuous", default=False)

    class Meta:
        db_table = 'map_sensor_type'
        verbose_name = "sensor type"
        verbose_name_plural = "sensor types"
        ordering = ["name"]

    def __unicode__(self):
        return self.name


class SensorStatus(models.Model):
    type = models.ForeignKey(SensorType, verbose_name='type', related_name='statuses')
    name = models.CharField("status", max_length=50)
    msg = models.TextField("message")
    icon = models.CharField("icon", max_length=255)
    is_enabled = models.BooleanField("is enabled", default=True)
    value = models.IntegerField('value', blank=True, null=True)
    min_value = models.IntegerField("min value", blank=True, null=True)
    max_value = models.IntegerField("max value", blank=True, null=True)

    class Meta:
        db_table = 'map_sensor_status'
        verbose_name = "sensor status"
        verbose_name_plural = "sensor status"
        ordering = ["type", "name"]

    def __unicode__(self):
        return "%s: %s" % (self.type.name, self.name)


class Sensor(models.Model):
    floor = models.ForeignKey(Floor, verbose_name="floor", related_name="sensors")
    type = models.ForeignKey(SensorType, verbose_name="type", related_name="sensors")
    description = models.TextField("description", blank=True, null=True)
    date_created = models.DateTimeField("date created", auto_now_add=True)
    date_updated = models.DateTimeField("date updated", auto_now=True)
    # This columns are saved by event_manager
    current_value = models.PositiveIntegerField("current value", default=0)
    current_pos_x = models.PositiveIntegerField("current X position in map", default=0)
    current_pos_y = models.PositiveIntegerField("current Y position in map", default=0)
    current_date = models.DateTimeField("current date")

    class Meta:
        verbose_name = "sensor"
        verbose_name_plural = "sensors"
        ordering = ["floor"]

    def __unicode__(self):
        return "%s" % (self.description or 'Private asset')

    def get_status(self):
        try:
            if self.type.is_continuous:
                status = self.type.statuses.filter(min_value__lte=self.current_value, max_value__gte=self.current_value)[:1].get()
            else:
                status = self.type.statuses.filter(value=self.current_value)[:1].get()
        except SensorStatus.DoesNotExist:
            status = None
        finally:
            return status
