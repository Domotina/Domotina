from django.db import models
from map.models import Sensor, SensorStatus, SensorType
# Create your models here.

class Rule(models.Model):
    sensor = models.ForeignKey(Sensor)
    status = models.ForeignKey(SensorStatus)
    description = models.CharField("description",max_length=255)

    class Meta:
        db_table = 'rule_engine_rule'
        verbose_name = "rule"
        verbose_name_plural = "rules"

    def __unicode__(self):
        return "%s: %s" % (self.sensor, self.status.name)

class Schedule(models.Model):
    sensor = models.ForeignKey(Sensor)
    begin_time = models.DateTimeField("begin")
    end_time = models.DateTimeField("end")
    description = models.CharField("Schedule Description", max_length=255)

    class Meta:
        db_table = 'rule_engine_schedule'
        verbose_name = "Schedule"
        verbose_name_plural = "Schedules"

    def __unicode__(self):
        return "%s %s %s %s" % (self.sensor, self.begin_time, self.end_time, self.description)

class ActionType(models.Model):
    name = models.CharField("action", max_length=50)

    class Meta:
        db_table = 'rule_engine_action_type'
        verbose_name = "Action Type"
        verbose_name_plural = "Action Types"

    def __unicode__(self):
        return self.name

class Action(models.Model):
    action = models.ForeignKey(ActionType)
    rule = models.ForeignKey(Rule,blank=True,null=True)
    schedule = models.ForeignKey(Schedule,blank=True,null=True)
    message = models.CharField("message",max_length=255)

    class Meta:
        db_table = 'rule_engine_action'
        verbose_name = "Action"
        verbose_name_plural = "Actions"

    def __unicode__(self):
        str = ""
        if self.rule is not None:
            str = "%s %s " % (self.action.name, self.rule)
        else:
            str = "%s %s " % (self.action.name, self.schedule)

        return str