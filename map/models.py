from datetime import timedelta, time, datetime

from django.db import models
from django.contrib.auth.models import User


def datetime_to_js(dt):
    return "new Date(%(year)s, %(month)s, %(day)s, %(h)s, %(m)s, %(s)s)" \
           % {'year': dt.strftime("%Y"),
              'month': dt.strftime("%m"),
              'day': dt.strftime("%d"),
              'h': dt.strftime("%H"),
              'm': dt.strftime("%M"),
              's': dt.strftime("%S")}


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

    def get_sensors_json(self, sensor_type=None):
        sensors_array = []
        floors = self.floors.order_by("number")
        for floor in floors:
            sensors_array.extend(floor.get_sensors_json(sensor_type))
        return sensors_array

    def snapshot(self, date=None, json=False, include_events=False):
        sensors_array = []
        floors = self.floors.order_by("number")
        for floor in floors:
            sensors_array.extend(floor.snapshot(date=date, json=json, include_events=include_events))
        return sensors_array

    def floors_to_json(self):
        floors = []
        for floor in self.floors.order_by("number"):
            floors.append(floor.to_json())
        return floors


class Floor(models.Model):
    place = models.ForeignKey(Place, verbose_name="place", related_name="floors")
    number = models.PositiveIntegerField("number", default=1)
    map = models.CharField("map image", max_length=255)
    date_created = models.DateTimeField("date created", auto_now_add=True)
    date_updated = models.DateTimeField("date updated", auto_now_add=True)

    class Meta:
        verbose_name = "floor"
        verbose_name_plural = "floors"
        ordering = ["place", "number"]

    def __unicode__(self):
        return "%s Floor %s" % (self.place, self.number)

    def to_json(self):
        return '{number: %d, url: "%s"}' % (self.number, self.map)

    def get_sensors_json(self, sensor_type=None, include_events=False):
        sensors_array = []
        if sensor_type is None:
            sensors = self.sensors.get_queryset()
        else:
            sensors = self.sensors.filter(type=sensor_type)

        for sensor in sensors:
            sensor_json = sensor.to_json(include_events)
            if sensor_json:
                sensors_array.append(sensor_json)
        return sensors_array

    def snapshot(self, date=None, json=False, include_events=False):
        sensors_array = []
        creation_date = date + timedelta(days=1)
        if date is not None:
            sensors = self.sensors.filter(date_created__lte=creation_date)
        else:
            sensors = self.sensors.get_queryset()
        for sensor in sensors:
            sensor = sensor.snapshot(date=date, json=json, include_events=include_events)
            if sensor:
                sensors_array.append(sensor)
        return sensors_array


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
    current_value = models.PositiveIntegerField("current value", default=0)
    current_pos_x = models.PositiveIntegerField("current X position in map", default=0)
    current_pos_y = models.PositiveIntegerField("current Y position in map", default=0)
    current_date = models.DateTimeField("current date", auto_now_add=True)

    class Meta:
        verbose_name = "sensor"
        verbose_name_plural = "sensors"
        ordering = ["floor"]

    def __unicode__(self):
        return "%s" % (self.description or 'Private asset')

    def get_status(self):
        status = None
        try:
            if self.type.is_continuous:
                status = self.type.statuses.filter(min_value__lte=self.current_value,
                                                   max_value__gte=self.current_value)[:1].get()
            else:
                status = self.type.statuses.filter(value=self.current_value)[:1].get()
        except SensorStatus.DoesNotExist:
            status = None
        finally:
            return status

    def to_json(self, date=None, include_events=False):
        status = self.get_status()
        if status is None:
            return ''
        sensor = '{status: "%s", url: "%s", posX: %d, posY: %d, ' \
                 'description: "%s", floor: %d, creationDate: %s' \
                 % (status.name,
                    status.icon,
                    self.current_pos_x,
                    self.current_pos_y,
                    self,
                    self.floor.number,
                    datetime_to_js(self.date_created))
        if include_events:
            sensor += ', events: [%s]}' % (','.join(self.events_to_json(date=date)))
        else:
            sensor += '}'
        return sensor

    def snapshot(self, date=None, json=False, include_events=False):
        if date is not None:
            tmp_value = False
            tmp_x = False
            tmp_y = False
            events = self.event_set.filter(timestamp__lte=date).order_by("-timestamp")
            for event in events:
                if event.value is not None and not tmp_value:
                    self.current_value = event.value
                    tmp_value = True
                if event.pos_x is not None and not tmp_x:
                    self.current_pos_x = event.pos_x
                    tmp_x = True
                if event.pos_y is not None and not tmp_y:
                    self.current_pos_y = event.pos_y
                    tmp_y = True
                if tmp_value and tmp_x and tmp_y:
                    break
        if json:
            return self.to_json(date=date, include_events=include_events)
        else:
            return self

    def events_to_json(self, date=None):
        events_array = []
        if date is None:
            events = self.event_set.order_by("-timestamp")
        else:
            limit = date + timedelta(days=1)
            events = self.event_set.filter(timestamp__gte=date, timestamp__lt=limit).order_by("-timestamp")
        for event in events:
            event_json = event.to_json()
            if event_json:
                events_array.append(event_json)
        return events_array


class ZoomLocation(models.Model):
    floor = models.ForeignKey(Floor, verbose_name="floor", related_name="zoom")
    pos_x = models.PositiveIntegerField("X position in map", default=0)
    pos_y = models.PositiveIntegerField("Y position in map", default=0)
    width_zoom = models.PositiveIntegerField("Width zoom", default=0)
    heigth_zoom = models.PositiveIntegerField("Heigth zoom", default=0)

    class Meta:
        ordering = ["floor"]

