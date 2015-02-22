from django.shortcuts import render, get_object_or_404
from models import Place, Door, Window
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
            var ctx = c.getContext("2d");';
    place = get_object_or_404(Place, pk=pk)

    # Get all doors in current place
    doors = Door.objects.filter(place=place)
    for door in doors:
        lock_icon = "unlock_icon.png";
        if door.is_locked:
            lock_icon = "lock_icon.png";
        show_icons_script = \
            '%s var door_icon%s  = new Image(); \
                door_icon%s.src = "%simg/%s"; \
                ctx.drawImage(door_icon%s, %s, %s);' \
                % (show_icons_script, door.id, door.id, server_path, lock_icon,
                   door.id, door.coord_x, door.coord_y)

    # Get all windows in current place
    windows = Window.objects.filter(place=place)
    for window in windows:
        lock_icon = "unlock_icon.png";
        if window.is_locked:
            lock_icon = "lock_icon.png";
        show_icons_script = \
            '%s var window_icon%s  = new Image(); \
                window_icon%s.src = "%simg/%s"; \
                ctx.drawImage(window_icon%s, %s, %s);' \
                % (show_icons_script, window.id, window.id, server_path, lock_icon,
                   window.id, window.coord_x, window.coord_y)

    show_icons_script = show_icons_script + '});';

    # Split map page into its filename and extension
    map_page = '%s://%s/%s%s' % (request.META['wsgi.url_scheme'], request.META['HTTP_HOST'],
                                          settings.UPLOADED_FILE_PATH[4:len(settings.UPLOADED_FILE_PATH)],
                                          place.map)
    filename, file_ext = splitext(basename(urlparse(map_page).path))

    context = {'place': place, 'show_icons_script': show_icons_script,
               'map_url': '%s://%s/%s%s%s' % (request.META['wsgi.url_scheme'], request.META['HTTP_HOST'],
                                          settings.UPLOADED_FILE_PATH[4:len(settings.UPLOADED_FILE_PATH)],
                                          filename, file_ext)}
    return render(request, 'myplaces.html', context)