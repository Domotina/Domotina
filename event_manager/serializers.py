from rest_framework import serializers
from .models import Event, EventType
from map.models import Sensor


class EventSerializer(serializers.HyperlinkedModelSerializer):
    sensor = serializers.PrimaryKeyRelatedField(queryset=Sensor.objects.all())
    type = serializers.PrimaryKeyRelatedField(queryset=EventType.objects.all())

    class Meta:
        model = Event
        fields = ('id', 'timestamp', 'type', 'sensor', 'pos_x', 'pos_y', 'value')
