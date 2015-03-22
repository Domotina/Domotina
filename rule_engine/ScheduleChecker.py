import traceback
from map.models import SensorStatus
from .models import ScheduleDaily
from event_manager.models import Alarm
from django.core.mail import EmailMessage
from domotina.settings import EMAIL_HOST_USER, URL
from django.utils.html import format_html
from django.template import defaultfilters
import threading
"""
Description: check_schedule is method designed to check if a event has broken a rule defined by the owner of a property.
Version: 1.0.0
Creation date: 20/03/2015
Autor: Luis Felipe Mendivelso Osorio
Last modification: 20/03/2015
Modify by: No one
"""

def create_checker(event):
    d = threading.Thread(name='daemon', target=check_schedule(event))
    d.setDaemon(True)
    try:
        d.start()
    except:
        print ("Error in check_schedule.")
        print traceback.format_exc()
        d.join()


def check_schedule(event):
    # Search the sensor status of the event
    status = SensorStatus.objects.filter(value=event.value,type=event.sensor.type)[0]
    # Search all daily schedule with status and sensor of the event
    schedules = ScheduleDaily.objects.filter(status=status, sensor=event.sensor)
    # If sensor has schedules to check, then check if any has broken a rule defined by the owner or domotina's central.
    if schedules:
        for schedule in schedules:
            # If sensor status on the event is between time intervals that is not allowed to using, then generate a alarm.
            if (event.timestamp.time() > schedule.begin_time) & (event.timestamp.time() < schedule.end_time):
                try:
                    # Check the type of action to take on schedule
                    if schedule.actionType.id == 1:
                        # Create a alarm
                        alarm=Alarm(event=event,activation_date=event.timestamp,activated=True,notified=False)
                        # Create a email with alarm and schedule information
                        email = create_email(alarm,schedule)
                        # Send the notification according of type of action.
                        email.send()
                except:
                    print ("Error in check_schedule.")
                    print traceback.format_exc()

                print ("A schedule was checked and processed")

            else:
                print ("The sensor is OK with the rule: "+ str(schedule))
    else:
        print ("The sensor event does not have schedules.")

def create_email(alarm, schedule):
    title = u"Event notification"
    text = u"An alarm has been triggered in your property. Please read carefully the following information:"
    place = str(alarm.event.sensor.floor.place.name)
    timestamp = defaultfilters.date(alarm.event.timestamp, "SHORT_DATETIME_FORMAT")
    event_type = str(alarm.event.type.name)
    asset = str(alarm.event.sensor.description)
    description = schedule.message
    msg = u"<html><head><meta charset='UTF-8'><style>table, th, td {{border: 1px solid black;border-collapse: collapse;}}th,td {{padding: 10px;}}table tr:nth-child(even) {{background-color: #eee;}}table tr:nth-child(odd) {{background-color:#fff;}}table th	{{background-color: black;color: white;}}</style></head>"
    msg = msg + u"<body><h1><b>{0}</b></h1><p>{1}</p>"
    msg = msg + u"<table>"
    msg = msg + u"<tr><td>Place:</td><td>{2}</td></tr>"
    msg = msg + u"<tr><td>Timestamp:</td><td>{3}</td></tr>"
    msg = msg + u"<tr><td>Type of event:</td><td>{4}</td></tr>"
    msg = msg + u"<tr><td>Asset:</td><td>{5}</td></tr>"
    msg = msg + u"<tr><td>Description:</td><td>{6}</td></tr>"
    msg = msg + u"</table>"
    msg = msg + u"<p>Please login in your account to manage this event. <a href='{7}'>Domotina</a></p>"
    msg = msg + u"<img src='http://kunagi-domotina.rhcloud.com/kunagi/kunagi.png'></html>"
    html = format_html(msg, title, text, place, timestamp, event_type, asset, description, URL)
    email = EmailMessage(u'Event notification', html, EMAIL_HOST_USER, [alarm.event.sensor.floor.place.owner.email])
    email.content_subtype = "html"
    return email