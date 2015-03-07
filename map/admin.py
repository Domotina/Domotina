from django.contrib import admin
from models import Neighborhood, Place, Asset, SensorType, SensorStatus, Sensor

admin.site.register(Neighborhood)
admin.site.register(Place)
admin.site.register(Asset)
admin.site.register(SensorType)
admin.site.register(SensorStatus)
admin.site.register(Sensor)