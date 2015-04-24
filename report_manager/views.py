from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.messages import error
from xhtml2pdf import pisa
from django.http import HttpResponse
from django.template import RequestContext
from django.template.loader import render_to_string

from map.models import Place
from event_manager.models import Event

import calendar
from datetime import datetime, date
import cStringIO as StringIO
import cgi


def home(request, place_pk):
    # Getting the place
    place = get_object_or_404(Place, pk=place_pk)

    context = {'place': place}
    return render(request, 'form.html', context)


def generate_pdf(html):
    # Generic function to generate a pdf file
    result = StringIO.StringIO()
    pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("UTF-8")), result, link_callback=fetch_resources)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return HttpResponse('PDF document cannot be generated: %s' % cgi.escape(html))


def fetch_resources(uri, rel):
    import os.path
    from django.conf import settings
    path = os.path.join("index/static", uri.replace(settings.STATIC_URL, ""))

    return path


def events_in_date_range(request, place_pk):
    # Scenario 1 is validated displaying a message when have no results!
    # Scenario 2 is validated displaying all events in a place between a date range! (Ideal scenario)
    # Scenario 3 and 4 are validated via js, indicating dates are required fields!

    start_year = 0
    end_year = 0
    if request.method == 'POST':
        # Validating if dates are in valid format!
        try:
            start_year = datetime.strptime(request.POST['start_date'], "%Y-%m-%d").year
        except ValueError:
            error(request, "The start date must be with valid format.")
            return redirect('report_home', place_pk=place_pk)

        try:
            end_year = datetime.strptime(request.POST['end_date'], "%Y-%m-%d").year
        except ValueError:
            error(request, "The end date must be with valid format.")
            return redirect('report_home', place_pk=place_pk)

        start_date = request.POST['start_date']
        end_date = request.POST['end_date']
        as_pdf = request.POST['output'] != 'html'

    else:
        return redirect('report_home', place_pk=place_pk)

    # Scenario 5 is validated redirecting to form page and indicating that
    # end date must be greater than start date
    if datetime.strptime(start_date, "%Y-%m-%d") > \
            datetime.strptime(end_date, "%Y-%m-%d"):
        error(request, "The end date must be greater than the start date.")
        return redirect('report_home', place_pk=place_pk)


    if not start_year > 1900:
        error(request, "The year in the start date must be greater than 1900.")
        return redirect('report_home', place_pk=place_pk)

    if not end_year > 1900:
        error(request, "The year in the end date must be greater than 1900.")
        return redirect('report_home', place_pk=place_pk)


    start_month = datetime.strptime(start_date, "%Y-%m-%d").month
    end_month = datetime.strptime(end_date, "%Y-%m-%d").month

    if not start_month in range(1, 13):
        error(request, "The month in the start date must be between 1 and 12.")
        return redirect('report_home', place_pk=place_pk)

    if not end_month in range(1, 13):
        error(request, "The month in the end date must be between 1 and 12.")
        return redirect('report_home', place_pk=place_pk)


    start_day = datetime.strptime(start_date, "%Y-%m-%d").day
    end_day = datetime.strptime(end_date, "%Y-%m-%d").day

    if start_day <= 0 or start_day >= 30:
        start_day = 1

    if end_day <= 0 or end_day >= 30:
        end_day = calendar.monthrange(end_year, end_month)[1]


    # Getting the place to filter events
    place = get_object_or_404(Place, pk=place_pk)

    # Filtering events in a place and a in a date range
    events = Event.objects.filter(sensor__floor__place=place)\
        .filter(timestamp__gt=date(start_year, start_month, start_day),
                timestamp__lt=date(end_year, end_month, end_day)).order_by('-timestamp')

    context = {'place': place, 'events': events,
               'start_date': start_date, 'end_date': end_date}

    # Generating pdf file
    if as_pdf and events:
        html = render_to_string('events_in_date_range_pdf.html', {'pagesize':'A4', 'place': place, 'events': events,
               'start_date': start_date, 'end_date': end_date}, context_instance=RequestContext(request))
        return generate_pdf(html)

    # Displaying report in HTML
    return render(request, 'events_in_date_range.html', context)