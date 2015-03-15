from django.contrib import admin
from models import Neighborhood, Place, Asset, SensorType, SensorStatus, Sensor


class PlaceAdmin(admin.ModelAdmin):
    list_display = ("owner", "neighborhood", "name", "map")
    list_editable = ("name", "map")
    list_filter = ("owner", "neighborhood", "name", "map")
    search_fields = ("owner", "neighborhood", "name", "map")


class AssetAdmin(admin.ModelAdmin):
    list_display = ("get_neighborhood", "place", "name")
    list_editable = ("name", )
    list_filter = ("place", "name", "description")
    search_fields = ("place", "name", "description")

    def get_neighborhood(self, obj):
        return '%s' % (obj.place.neighborhood)
    get_neighborhood.short_description = 'Neighborhood'


class SensorAdmin(admin.ModelAdmin):
    list_display = ("get_place", "asset", "current_status_id", "current_pos_x", "current_pos_y")
    list_editable = ("current_status_id", "current_pos_x", "current_pos_y")
    list_filter = ("asset", "type", "description")
    search_fields = ("asset", "type", "description")

    def get_place(self, obj):
        return '%s %s' % (obj.asset.place.neighborhood, obj.asset.place)
    get_place.short_description = 'Place'


admin.site.register(Neighborhood)
admin.site.register(Place, PlaceAdmin)
admin.site.register(Asset, AssetAdmin)
admin.site.register(SensorType)
admin.site.register(SensorStatus)
admin.site.register(Sensor, SensorAdmin)