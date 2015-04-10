# coding=UTF-8
from django.core.mail import EmailMessage
from django.utils.html import format_html

from domotina.settings import EMAIL_HOST_USER, URL


def create_email(user):
    title = u"Your account has been created"
    text = u"A user has been created for you with the following data:"

    msg = u"<html><head><meta charset='UTF-8'><style>table, th, td {{border: 1px solid black;border-collapse: collapse;}}th,td {{padding: 10px;}}table tr:nth-child(even) {{background-color: #eee;}}table tr:nth-child(odd) {{background-color:#fff;}}table th	{{background-color: black;color: white;}}</style></head>"
    msg = msg + u"<body><h1><b>{0}</b></h1><p>{1}</p>"
    msg = msg + u"<table>"
    msg = msg + u"<tr><td>Username:</td><td>{2}</td></tr>"
    msg = msg + u"<tr><td>First Name:</td><td>{3}</td></tr>"
    msg = msg + u"<tr><td>Last Name:</td><td>{4}</td></tr>"
    msg = msg + u"<tr><td>Email:</td><td>{5}</td></tr>"
    msg = msg + u"<tr><td>Password:</td><td>{6}</td></tr>"
    msg = msg + u"</table>"
    msg = msg + u"<p>Please login in your account to manage this event. <a href='{7}'>Domotina</a></p>"
    msg = msg + u"<img src='http://kunagi-domotina.rhcloud.com/kunagi/kunagi.png'></html>"
    html = format_html(msg, title, text, user.username, user.first_name, user.last_name, user.email, 'DOMOTINA123', URL)
    email = EmailMessage(u'New account on Domotina', html, EMAIL_HOST_USER, [user.email])
    email.content_subtype = "html"
    return email


def send_email(user):
    if EMAIL_HOST_USER is not None:
        email = create_email(user)
        email.send()