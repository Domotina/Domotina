from django.shortcuts import render, get_object_or_404
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
    server_path = "%s://%s%s" % (request.META['wsgi.url_scheme'], request.META['HTTP_HOST'], settings.STATIC_URL)

    # TODO: Check if the current user has permission to view this place

    show_icons_script = \
        '$(document).ready(function() { \
        var c = document.getElementById("place_canvas"); \
        var ctx = c.getContext("2d");'
    place = get_object_or_404(Place, pk=pk)

    # Get all assets in the current place
    assets = Asset.objects.filter(place=place)
    for asset in assets:
        sensors = Sensor.objects.filter(asset=asset)
        for sensor in sensors:
            # Get the sensor status based on current_status_id saved by event_manager previously
            try:
                status = SensorStatus.objects.get(id=sensor.current_status_id)
                #filename, file_ext = splitext(basename(str(status.icon)))
                show_icons_script = \
                    '%s var sensor_icon%s  = new Image();' \
                    'sensor_icon%s.src = "%s"; \
                    ctx.drawImage(sensor_icon%s, %s, %s);' \
                    % (show_icons_script, sensor.id,
                       sensor.id, status.icon, #server_path, filename, file_ext,
                       sensor.id, sensor.current_pos_x, sensor.current_pos_y)
            except SensorStatus.DoesNotExist:
                pass

    show_icons_script = show_icons_script + '});';

    '''# Split map place url into its filename and extension
    filename, file_ext = splitext(basename(str(place.map)))
    map_url = '%s://%s/%s%s%s' % (request.META['wsgi.url_scheme'], request.META['HTTP_HOST'],
                                  settings.MAP_FILE_PATH[4:len(settings.MAP_FILE_PATH)],
                                          filename, file_ext)'''

    alarms = Alarm.objects.filter(event__sensor__asset__place__owner=request.user).order_by('-activation_date')
    events = Event.objects.filter(sensor__asset__place__owner=request.user).order_by('-timestamp')

    context = {'place': place, 'show_icons_script': show_icons_script,
               'map_url': place.map, 'events': events, 'alarms': alarms}
    return render(request, 'index_owner.html', context)
