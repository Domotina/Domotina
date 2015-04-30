from datetime import datetime, time

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import permission_required
from rest_framework import viewsets

from middleware.http import Http403
from .models import Place, Floor, Sensor, SensorType, Neighborhood, Delegate
from .serializers import SensorSerializer
from event_manager.models import Event, Alarm

# user.has_perm('map.add_place') es el permiso minimo para entrar a my_places
def user_can_see(user):
    return user.is_superuser or user.groups.filter(name='UsersOwners').exists() or user.has_perm('map.add_place')
def user_can_see_central(user):
    return user.groups.filter(name='UsersCentral').exists()


def paginator(qs, page, items_per_page):
    paginator_instance = Paginator(qs, items_per_page)
    try:
        result = paginator_instance.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        result = paginator_instance.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        result = paginator_instance.page(paginator_instance.num_pages)
    return result


@login_required
#@user_passes_test(user_can_see, login_url='/')
#@user_passes_test(user_can_see_central, login_url='/central/')
#@permission_required('map.add_place', login_url='/map/')
def my_places(request):

    if request.user.has_perm('map.add_place') == False and request.user.groups.filter(name='UsersOwners').exists() == False:
        raise Http403

    if request.user.groups.filter(name='UsersOwners').exists():
        places = Place.objects.filter(owner=request.user)
        context = {'user': request.user, 'places': places}
        return render(request, 'myplaces.html', context)
    else:
        placesDelegate = Delegate.objects.all().filter(delegate=request.user)
        print placesDelegate
        place = []
        for item in placesDelegate:
            place.append(item.getPlace())
            print item.getPlace()

        context = {'user': request.user, 'places': place}
        return render(request, 'myplaces.html', context)


@login_required
def place_view(request, pk):
    place = get_object_or_404(Place, pk=pk)

    #if request.user != place.owner:
        #raise Http403

    floors = paginator(place.floors.order_by("number"), request.GET.get("floor_page"), 1)
    current_floor = floors.object_list[0]

    events = paginator(Event.objects.filter(sensor__floor=current_floor).order_by('-timestamp'),
                       request.GET.get('event_page'), 5)
    alarms = paginator(Alarm.objects.filter(event__sensor__floor=current_floor).order_by('-event__timestamp'),
                       request.GET.get('alarm_page'), 5)

    sensor_type = request.GET.get('type') and SensorType.objects.get(pk=request.GET.get('type'))

    sensors_json = ','.join(current_floor.get_sensors_json(sensor_type=sensor_type))

    zoom_json = ','.join(current_floor.get_zoom_json())

    types = SensorType.objects.all()

    current_date = datetime.now().strftime("%Y%m%d")

    context = {'floor': current_floor, 'sensors': sensors_json, 'floors': floors,
               'events': events, 'alarms': alarms, 'types': types,
               'type': sensor_type, 'now': current_date, 'zoom': zoom_json}
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


# Metodos para Administracion de urbanizaciones y/o edificios

# @login_required
def list_neighborhoods(request):
    # TO-DO
    # Modificar, solo valido para las pruebas iniciales

    # Deberia retrnar un query set
    neighborhoods = []
    n1 = Neighborhood(name="name1")
    n2 = Neighborhood(name="name1")
    neighborhoods.append(n1)
    neighborhoods.append(n2)
    return render(request, 'neighborhood.html', {'neighborhoods': neighborhoods})


# @login_required
def create_neighborhood(request):
    # TO-DO, implementacion temporal valida solo para las pruebas iniciales
    # print(request)
    print(request.POST['name'])
    # Render temporal, solo importa el context
    return render(request, 'neighborhood.html', {'created': True})


# @login_required
def delete_neighborhood(request, neighborhood_pk):
    # TO-DO, implementacion temporal valida solo para las pruebas iniciales
    # print(request)
    print(neighborhood_pk)
    # Render temporal, solo importa el context
    return render(request, 'neighborhood.html', {'deleted': True})


# @login_required
def edit_neighborhood(request, neighborhood_pk):
    neighborhood = get_object_or_404(Neighborhood, pk=neighborhood_pk)
    return render(request, 'neighborhood.html', {'edited': True, 'neighborhood': neighborhood})


@login_required
def map_history(request, place_pk, int_date):
    date = datetime.combine(datetime.today(), time(0))
    try:
        date = datetime.strptime(int_date, "%Y%m%d")
    except ValueError:
        pass
    init_date = "new Date('%(year)s %(month)s %(day)s')" \
                % {'year': date.strftime("%Y"),
                   'month': date.strftime("%m"),
                   'day': date.strftime("%d")}
    place = get_object_or_404(Place, pk=place_pk)
    floors = ','.join(place.floors_to_json())
    sensors = ','.join(place.snapshot(date=date, json=True, include_events=True))

    events = Event.objects.filter(sensor__floor__place=place).order_by('-timestamp')
    return render(request, "historic_map.html", {'place': place,
                                                 'events': events,
                                                 'floors': floors,
                                                 'sensors': sensors,
                                                 'datetime': init_date})


class SensorViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows sensors to be viewed or edited.
    """
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer

