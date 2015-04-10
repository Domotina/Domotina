from rest_framework import serializers
from .models import Event
from map.models import Sensor


class EventSerializer(serializers.HyperlinkedModelSerializer):
    sensor = serializers.PrimaryKeyRelatedField(queryset=Sensor.objects.all())

    class Meta:
        model = Event
        fields = ('id', 'timestamp', 'sensor', 'pos_x', 'pos_y', 'value')
