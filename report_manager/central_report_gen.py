import datetime
import calendar

def validation_entry(year, month,list):
    validate = True

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


def events_from_place(start,end,place):
    events = []

    return events

def find_events(start, end, list):
    events = []

    return events

def generate_report():
    report = ""