from django.contrib import admin
from . import models
# Register your models here.
admin.site.register(models.ActionType)
admin.site.register(models.Rule)
admin.site.register(models.Schedule)
admin.site.register(models.Action)