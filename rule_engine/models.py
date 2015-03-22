from django.db import models
from map.models import Sensor, SensorStatus

"""
Model: ActionType
Description: ActionType is a model created to define the kind of actions that Domotina could do it, when a rules of schedule is not fulfilled.
Version: 1.0.0
Creation date: 20/03/2015
Autor: Luis Felipe Mendivelso Osorio
Last modification: 20/03/2015
Modify by: No one
"""
class ActionType(models.Model):
    name = models.CharField("action", max_length=50)

    class Meta:
        db_table = 'rules_action_type'
        verbose_name = "Action Type"
        verbose_name_plural = "Action Types"

    def __unicode__(self):
        return self.name

"""
Model: ScheduleDaily
Description: This model is designed to manage the daily schedules for assets or sensors located in his/her property, with the purpose of define the rules of using and actions to take in cases which the rule is not fulfilled.
Version: 1.0.0
Creation date: 20/03/2015
Autor: Luis Felipe Mendivelso Osorio
Last modification: 20/03/2015
Modify by: No one
"""
class ScheduleDaily(models.Model):
    sensor = models.ForeignKey(Sensor)
    status = models.ForeignKey(SensorStatus)
    begin_time = models.TimeField("begin")
    end_time = models.TimeField("end")
    actionType = models.ForeignKey(ActionType)

    class Meta:
        db_table = 'rules_schedule_daily'
        verbose_name = "Daily Schedule"
        verbose_name_plural = "Daily Schedules"

    def __unicode__(self):
        return "Sensor: %s -> %s - %s. Action: %s" % (self.sensor, self.begin_time, self.end_time,self.actionType)