from rest_framework import serializers
from .models import Event, EventType
from sensor.models import Sensor
class EventSerializer(serializers.HyperlinkedModelSerializer):
    sensor = serializers.PrimaryKeyRelatedField(queryset=Sensor.objects.all())

    class Meta:
        model = Event
        fields = ('id', 'timestamp', 'type', 'sensor', 'pos_x', 'pos_y')

class EventTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = EventType
        fields = ('id','name','description', 'is_critical')