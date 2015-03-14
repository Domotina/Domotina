from django.shortcuts import render, get_object_or_404
from middleware.http import Http403
from models import Place, Asset, Sensor, SensorStatus
from event_manager.models import Event, Alarm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

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
    alarm_qs = Alarm.objects.filter(event__sensor__asset__place=place).order_by('-activation_date')
    event_qs = Event.objects.filter(sensor__asset__place=place).order_by('-timestamp')

    events_paginator = Paginator(event_qs, 5)
    page = request.GET.get('event_page')
    try:
        events = events_paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        events = events_paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        events = events_paginator.page(events_paginator.num_pages)

    alarms_paginator = Paginator(alarm_qs, 5)
    page = request.GET.get('alarm_page')
    try:
        alarms = alarms_paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        alarms = alarms_paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        alarms = alarms_paginator.page(alarms_paginator.num_pages)

    context = {'place': place, 'sensors': sensors_json,
               'map_url': place.map, 'events': events, 'alarms': alarms}
    return render(request, 'index_owner.html', context)
