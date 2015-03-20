from django.contrib import admin
from . import models
# Register your models here.
"""
Description: Admin.py have references of models and functions that the Django Admin module have to manage corresponding to Rule Engine.
Version: 1.0.0
Creation date: 20/03/2015
Autor: Luis Felipe Mendivelso Osorio
Last modification: 20/03/2015
Modify by: No one
"""

"""
Registration of ActionType model on Django admin module.
"""
admin.site.register(models.ActionType)
"""
Registration of ScheduleDaily model on Django admin module.
"""
admin.site.register(models.ScheduleDaily)
"""
Registration of Action model on Django admin module.
"""
admin.site.register(models.Action)