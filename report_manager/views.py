from django.shortcuts import render, redirect, get_object_or_404
from map.models import Place
from event_manager.models import Event

import time, datetime, calendar

def home(request, place_pk):
    print place_pk
    # Getting the place
    place = get_object_or_404(Place, pk=place_pk)
    context = {'place': place}
    return render(request, 'form.html', context)

def events_in_date_range(request, place_pk):

    if request.method == 'POST':
        if request.POST['start_date'] and request.POST['end_date']:
            start = request.POST['start_date'].replace("/", "")
            end = request.POST['end_date'].replace("/", "")
        else:
            return redirect('report_home', place_pk=place_pk)
    else:
        return redirect('report_home', place_pk=place_pk)


    # Start date and end date MUST BE a string with 8 characters length (i.e. 20150401)
    if len(start) != 8 or len(end) != 8:
        print "Formato de fecha invalido"
        return redirect('report_home', place_pk=place_pk)

    start_year = datetime.datetime.strptime(start, "%Y%m%d").year
    end_year = datetime.datetime.strptime(end, "%Y%m%d").year

    if not start_year > 1900 or not end_year > 1900:
        print "Formato de fecha invalido"
        return redirect('report_home', place_pk=place_pk)


    start_month = datetime.datetime.strptime(start, "%Y%m%d").month
    end_month = datetime.datetime.strptime(end, "%Y%m%d").month

    if not start_month in range(1,12) or not end_month in range(1,12):
        print "Formato de fecha invalido"
        return redirect('report_home', place_pk=place_pk)


    start_day = datetime.datetime.strptime(start, "%Y%m%d").day
    end_day = datetime.datetime.strptime(end, "%Y%m%d").day

    if start_day <= 0 or start_day >= 30:
        start_day = 1

    if end_day <= 0 or end_day >= 30:
        end_day = calendar.monthrange(end_year, end_month)[1]


    # Getting the place to filter events
    place = get_object_or_404(Place, pk=place_pk)

    # Filtering events in a place and a in a date range
    events = Event.objects.filter(sensor__floor__place=place)\
                            .filter(timestamp__gt=datetime.date(start_year, start_month, start_day),
                                    timestamp__lt=datetime.date(end_year, end_month, end_day))


    context = {'place': place, 'events': events,
               'start_date': request.POST['start_date'], 'end_date': request.POST['end_date']}
    return render(request, 'events_in_date_range.html', context)