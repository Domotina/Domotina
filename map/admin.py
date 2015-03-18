from django.contrib import admin
from models import Neighborhood, Place, Floor, SensorType, SensorStatus, Sensor


class PlaceAdmin(admin.ModelAdmin):
    list_display = ("owner", "neighborhood", "name")
    list_editable = ("name", )
    list_filter = ("owner", "neighborhood", "name")
    search_fields = ("owner", "neighborhood", "name")


class FloorAdmin(admin.ModelAdmin):
    list_display = ("get_neighborhood", "place", "number", "map")
    list_editable = ("number", "map")
    list_filter = ("place", "number", "map")
    search_fields = ("place", "number", "map")

    def get_neighborhood(self, obj):
        return obj.place.neighborhood
    get_neighborhood.short_description = 'Neighborhood'


'''class AssetAdmin(admin.ModelAdmin):
    list_display = ("get_neighborhood", "get_place", "name")
    list_editable = ("name", )
    list_filter = ("name", "description")
    search_fields = ("name", "description")

    def get_place(self, obj):
        return '%s' % (obj.floor.place)
    get_place.short_description = 'Place'

    def get_neighborhood(self, obj):
        return '%s' % (obj.place.neighborhood)
    get_neighborhood.short_description = 'Neighborhood'''''


class SensorAdmin(admin.ModelAdmin):
    list_display = ("get_place", "floor", "description", "current_status_id", "current_pos_x", "current_pos_y")
    list_editable = ("current_status_id", "current_pos_x", "current_pos_y")
    list_filter = ("floor", "type", "description")
    search_fields = ("floor", "type", "description")

    def get_place(self, obj):
        return '%s %s' % (obj.floor.place.neighborhood, obj.floor.place)
    get_place.short_description = 'Place'


admin.site.register(Neighborhood)
admin.site.register(Place, PlaceAdmin)
admin.site.register(Floor, FloorAdmin)
#admin.site.register(Asset, AssetAdmin)
admin.site.register(SensorType)
admin.site.register(SensorStatus)
admin.site.register(Sensor, SensorAdmin)