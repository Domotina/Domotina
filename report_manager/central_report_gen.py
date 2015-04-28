import datetime
import calendar
from django.shortcuts import get_object_or_404
from event_manager.models import Event
from map.models import Neighborhood, Place


def get_neighborhood():
    "This function is designed to get all neighborhood registered on Domotina"
    neighborhoods = Neighborhood.objects.all()
    return neighborhoods


def validation_entry(year, month):
    validate = True

    if not month in range(1, 12):
        validate = False
    if not year > 1900:
        validate = False
    return validate


def get_start_date(year, month):
    start_date = datetime.datetime(year, month, 1)
    return start_date


def get_end_date(year, month):
    month_range = calendar.monthrange(year, month)
    end_day = month_range[1]
    end_date = datetime.datetime(year, month, end_day)
    end_date = end_date.replace(hour=23, minute=59)
    return end_date


def events_from_place(start, end, place):
    events = Event.objects.filter(sensor__floor__place=place, timestamp__gt=start, timestamp__lt=end).order_by('-timestamp')
    return events


def find_events(start, end, places_id):
    events = []
    places = []
    if not places_id:
        places = Place.objects.all()
    else:
        for id in places_id:
            place = Place.objects.get(pk=id)
            places.append(place)

    for p in places:
        temp = events_from_place(start, end, p)
        if temp:
            events.extend(temp)

    return events

def are_events_to_report(events):
    if events:
        return True
    else:
        return False