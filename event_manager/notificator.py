# coding=UTF-8
from django.core.mail import EmailMessage
from domotina.settings import EMAIL_HOST_USER, URL
from django.utils.html import format_html
from django.template import defaultfilters

def create_email(alarm):
    title = u"Event notification"
    text = u"An alarm has been triggered in your property. Please read carefully the following information:"
    place = str(alarm.event.sensor.floor.place.name)
    timestamp = defaultfilters.date(alarm.event.timestamp, "SHORT_DATETIME_FORMAT")
    event_type = str(alarm.event.type.name)
    asset = str(alarm.event.sensor.description)
    description = str(alarm.event.type.description)
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


def send_email(alarm):
    if EMAIL_HOST_USER is not None:
        email = create_email(alarm)
        email.send()