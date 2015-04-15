import datetime
import calendar
from reportlab.pdfgen import canvas
from event_manager.models import Event

def validation_entry(year, month,places):
    validate = True
    if not month in range(1,12):
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


def events_from_place(start,end,places):
    events = []

    return events

def find_events(start, end, places):
    events = []
    if places:
        events = Event.objects.all()

    return events

def generate_report(events):
    generated = False
    if events:
        c = canvas.Canvas("Report.pdf")
        c.drawString(100,750,"Reporte de Eventos")
        #c.save()
        generated=True
        print "Se genero el report"
    else:
        print "No es posible generar el reporte"
        generated=False

    return generated