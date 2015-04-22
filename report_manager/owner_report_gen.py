import datetime
from map.models import Place
from event_manager.models import Event


# Validating if date is valid
def is_valid_format(date):
    passed = False
    try:
        start_year = datetime.datetime.strptime(date, "%Y/%m/%d").year
        passed = True
    except ValueError:
        passed = False

    return passed


# Getting the place based on its pk
def get_place(pk):
    return Place.objects.get(pk=pk)


# Getting events in the place based on a date range
def get_events_in_place(place, start_date, end_date):
    try:
        start_year = datetime.datetime.strptime(start_date, "%Y/%m/%d").year
        end_year = datetime.datetime.strptime(end_date, "%Y/%m/%d").year

        start_month = datetime.datetime.strptime(start_date, "%Y/%m/%d").month
        end_month = datetime.datetime.strptime(end_date, "%Y/%m/%d").month

        start_day = datetime.datetime.strptime(start_date, "%Y/%m/%d").day
        end_day = datetime.datetime.strptime(start_date, "%Y/%m/%d").day

        events = Event.objects.filter(sensor__floor__place=place)\
                            .filter(timestamp__gt=datetime.date(start_year, start_month, start_day),
                                    timestamp__lt=datetime.date(end_year, end_month, end_day))
        return events

    except ValueError:
        return None


# Verifying if the end date is greater than the start date
def is_end_date_greater(start_date, end_date):

    if datetime.datetime.strptime(start_date, "%Y/%m/%d") > \
            datetime.datetime.strptime(end_date, "%Y/%m/%d"):
        return False
    else:
        return True