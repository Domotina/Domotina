from django.shortcuts import render, get_object_or_404
from middleware.http import Http403
from models import Place, Floor, Sensor, SensorStatus, SensorType
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

    floor_qs = Floor.objects.filter(place=place).order_by("number")
    floor_paginator = Paginator(floor_qs, 1)
    page = request.GET.get("floor_page")
    try:
        floors = floor_paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        floors = floor_paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        floors = floor_paginator.page(floor_paginator.num_pages)


    current_floor = floors.object_list[0]

    if request.user != place.owner:
        raise Http403

    sensors_array = []
    type = request.GET.get('type')
    if type is not None:
        type_param = '&type='+type
        type = SensorType.objects.get(pk=type)
    else:
        type_param = ''

    if type is None:
        sensors = Sensor.objects.filter(floor=current_floor)
    else:
        sensors = Sensor.objects.filter(floor=current_floor, type=type)

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
    alarm_qs = Alarm.objects.filter(event__sensor__floor=current_floor).order_by('-activation_date')
    event_qs = Event.objects.filter(sensor__floor=current_floor).order_by('-timestamp')

    types = SensorType.objects.all()

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

    context = {'floor': current_floor, 'sensors': sensors_json, 'floors': floors,
               'events': events, 'alarms': alarms, 'types': types, 'type_param': type_param, 'type': type}
    return render(request, 'index_owner.html', context)
