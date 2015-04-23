from rest_framework import serializers
from .models import Sensor


class SensorSerializer(serializers.ModelSerializer):
    floor = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Sensor
        fields = ('id', '__unicode__', 'floor', 'current_value', 'current_pos_x', 'current_pos_y')
        read_only_fields = ('__unicode__',)
