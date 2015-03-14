from django.shortcuts import render, get_object_or_404
from middleware.http import Http403
from models import Place, Asset, Sensor, SensorStatus
from django.conf import settings
from event_manager.models import Event, Alarm
from django.contrib.auth.decorators import login_required

@login_required
def my_places(request):
    places = Place.objects.filter(owner=request.user)
    context = {'user': request.user, 'places': places}
    return render(request, 'myplaces.html', context)

@login_required
def place_view(request, pk):
    place = get_object_or_404(Place, pk=pk)

    if request.user != place.owner:
        raise Http403

    # Get all assets in the current place
    assets = Asset.objects.filter(place=place)
    sensors_array = []
    for asset in assets:
        sensors = Sensor.objects.filter(asset=asset)
        for sensor in sensors:
            # Get the sensor status based on current_status_id saved by event_manager previously
            try:
                status = sensor.type.sensorstatus_set.filter(ref_code=sensor.current_status_id)[:1].get()
                if status:
                    current_sensor = '{url: "%s",'\
                        'pos_x: %d,' \
                        'pos_y: %d}' \
                        % (status.icon, sensor.current_pos_x, sensor.current_pos_y)
                    sensors_array.append(current_sensor)
            except SensorStatus.DoesNotExist:
                pass

    sensors_json = ','.join(sensors_array)
    alarms = Alarm.objects.filter(event__sensor__asset__place=place).order_by('-activation_date')
    events = Event.objects.filter(sensor__asset__place=place).order_by('-timestamp')

    context = {'place': place, 'sensors': sensors_json,
               'map_url': place.map, 'events': events, 'alarms': alarms}
    return render(request, 'index_owner.html', context)
