from django.shortcuts import render, get_object_or_404
from models import Place, Asset, Sensor
from django.conf import settings
from urlparse import urlparse
from os.path import splitext, basename

def home(request):
    return render(request, 'index.html')

def place_view(request, pk):
    server_path = "%s://%s%s" % (request.META['wsgi.url_scheme'], request.META['HTTP_HOST'], settings.STATIC_URL)

    # TODO: Check if the current user has permission to view this place

    show_icons_script = \
        '$(document).ready(function() { \
        var c = document.getElementById("apartment_canvas"); \
        var ctx = c.getContext("2d");'
    place = get_object_or_404(Place, pk=pk)

    # Get all assets in current place
    assets = Asset.objects.filter(place=place)
    for asset in assets:
        sensors = Sensor.objects.filter(asset=asset)
        for sensor in sensors:
            filename, file_ext = splitext(basename(str(sensor.status.icon)))
            show_icons_script = \
                '%s var sensor_icon%s  = new Image(); \
                sensor_icon%s.src = "%simg/icons/%s%s"; \
                ctx.drawImage(sensor_icon%s, %s, %s);' \
                % (show_icons_script, sensor.id,
                   sensor.id, server_path, filename, file_ext,
                   sensor.id, sensor.pos_x, sensor.pos_y)

    show_icons_script = show_icons_script + '});';

    # Split map place url into its filename and extension
    filename, file_ext = splitext(basename(str(place.map)))
    map_url = '%s://%s/%s%s%s' % (request.META['wsgi.url_scheme'], request.META['HTTP_HOST'],
                                  settings.SENSOR_MAP_FILE_PATH[7:len(settings.SENSOR_MAP_FILE_PATH)],
                                          filename, file_ext)

    context = {'place': place, 'show_icons_script': show_icons_script,
               'map_url': map_url}
    return render(request, 'myplaces.html', context)
