from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse

from middleware.http import Http403
from models import Place, Floor, Sensor, SensorType, Neighborhood
from event_manager.models import Event, Alarm


def user_can_see(user):
    return user.is_superuser or user.groups.filter(name='UsersOwners').exists()


@login_required
@user_passes_test(user_can_see, login_url='/central/')
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
        type_param = '&type=' + type
        type = SensorType.objects.get(pk=type)
    else:
        type_param = ''

    if type is None:
        sensors = Sensor.objects.filter(floor=current_floor)
    else:
        sensors = Sensor.objects.filter(floor=current_floor, type=type)

    for sensor in sensors:
        status = sensor.get_status()
        if status:
            current_sensor = '{url: "%s",' \
                             'pos_x: %d,' \
                             'pos_y: %d,' \
                             'description: "%s",' \
                             'status: "%s"}' \
                             % (status.icon, sensor.current_pos_x, sensor.current_pos_y,
                                sensor.description, status.name)
            sensors_array.append(current_sensor)

    sensors_json = ','.join(sensors_array)

    # If there are sensors registered for this floor
    if sensors_array:
        sensors_json = ','.join(sensors_array)
    else:
        sensors_json = None

    alarm_qs = Alarm.objects.filter(event__sensor__floor=current_floor).order_by('-event__timestamp')
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
    return render(request, 'place_details.html', context)


@login_required
def list_sensors(request, place_pk):
    place = get_object_or_404(Place, pk=place_pk)
    sensors = Sensor.objects.filter(floor__place=place)
    return render(request, 'sensor_list.html', {'place': place, 'sensors': sensors})


@login_required
def create_sensor(request, place_pk):
    place = get_object_or_404(Place, pk=place_pk)
    types = SensorType.objects.all()
    floors = Floor.objects.filter(place=place)
    if request.method == 'POST':
        if request.POST['sensor_type'] and request.POST['floor'] and request.POST['description']:
            floor = get_object_or_404(Floor, pk=request.POST['floor'])
            sensor_type = get_object_or_404(SensorType, pk=request.POST['sensor_type'])
            sensor = Sensor(type=sensor_type, floor=floor, description=request.POST['description'])
            sensor.save()
            return redirect('list_sensors', place_pk=place_pk)
    return render(request, 'sensor_form.html', {'place': place, 'types': types, 'floors': floors})


@login_required
def edit_sensor(request, place_pk, sensor_pk):
    place = get_object_or_404(Place, pk=place_pk)
    sensor = get_object_or_404(Sensor, pk=sensor_pk)
    if request.method == 'POST':
        if request.POST['sensor_type'] and request.POST['floor'] and request.POST['description']:
            floor = get_object_or_404(Floor, pk=request.POST['floor'])
            sensor_type = get_object_or_404(SensorType, pk=request.POST['sensor_type'])
            sensor.type = sensor_type
            sensor.floor = floor
            sensor.description = request.POST['description']
            sensor.save()
            return redirect('list_sensors', place_pk=place_pk)
    types = SensorType.objects.all()
    floors = Floor.objects.filter(place=place)
    return render(request, 'sensor_form.html', {'place': place, 'types': types, 'floors': floors, 'sensor': sensor})


@login_required
def delete_sensor(request, place_pk, sensor_pk):
    sensor = get_object_or_404(Sensor, pk=sensor_pk)
    sensor.delete()
    return redirect('list_sensors', place_pk=place_pk)



#Metodos para Administracion de urbanizaciones y/o edificios

#@login_required
def list_neighborhoods(request):
    #TO-DO
    #Modificar, solo valido para las pruebas iniciales

    #Deberia retrnar un query set
    neighborhoods = []
    n1 = Neighborhood(name="name1")
    n2 = Neighborhood(name="name1")
    neighborhoods.append(n1)
    neighborhoods.append(n2)
    return render(request, 'neighborhood.html', {'neighborhoods': neighborhoods})

#@login_required
def create_neighborhood(request):
    #TO-DO, implementacion temporal valida solo para las pruebas iniciales
    #print(request)
    print(request.POST['name'])
    #Render temporal, solo importa el context
    return render(request, 'neighborhood.html', {'created': True})

#@login_required
def delete_neighborhood(request, neighborhood_pk):
    #TO-DO, implementacion temporal valida solo para las pruebas iniciales
    #print(request)
    print(neighborhood_pk)
    #Render temporal, solo importa el context
    return render(request, 'neighborhood.html', {'deleted': True})

#@login_required
def edit_neighborhood(request, neighborhood_pk):
    return render(request, 'neighborhood.html', {'edited': True})