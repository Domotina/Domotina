from datetime import datetime
import os
from django.core.mail import EmailMessage


def send_email(alarm):
    msg = "<html><style>table, th, td {border: 1px solid black;border-collapse: collapse;}th,td {padding: 10px;}table tr:nth-child(even) {background-color: #eee;}table tr:nth-child(odd) {background-color:#fff;}table th	{background-color: black;color: white;}</style><h1><b>Notificación de Evento</b> </h1><h3>Se ha generado una alerta en su inmueble, por favor lea con detenimiento la siguiente información:</h3>"
    msg = msg + "<table>"
    msg = msg + "<tr><td>Lugar: </td><td>"+str(alarm.event.sensor.place.name)+"</td></tr>"
    msg = msg + "<tr><td>Fecha y Hora: </td><td>"+str(alarm.event.timestamp)+"</td></tr>"
    msg = msg + "<tr><td>Tipo de Evento: </td><td>"+ str(alarm.event.type.name) +"</td></tr>"
    if alarm.event.sensor.asset:
        msg = msg + "<tr><td>Activo: </td><td>+"+ str(alarm.event.sensor.asset.name) +"</td></tr>"
    msg = msg + "<tr><td>Descripción: </td><td>"+ str(alarm.event.type.name) +"</td></tr>"
    msg = msg + "</table>"
    msg = msg + '<h3>Por favor ingrese a la plataforma de Domotina para gestionar este suceso.<a href="http://www.domotina.com/admin">Domotina.com</a></h3>'
    msg = msg + '<img src="http://kunagi-domotina.rhcloud.com/kunagi/kunagi.png"></html>'

    email = EmailMessage('Alarma Domotina', msg, os.environ.get('EMAIL_HOST_USER') ,[alarm.event.sensor.place.owner.email])
    email.content_subtype = "html"
    email.send()


def generate_email_test():

    msg = "<html><style>table, th, td {border: 1px solid black;border-collapse: collapse;}th,td {padding: 10px;}table tr:nth-child(even) {background-color: #eee;}table tr:nth-child(odd) {background-color:#fff;}table th	{background-color: black;color: white;}</style><h1><b>Notificación de Evento</b> </h1><h3>Se ha generado una alerta en su inmueble, por favor lea con detenimiento la siguiente información:</h3>"
    msg = msg + "<table>"
    msg = msg + "<tr><td>Fecha y Hora: </td><td>"+str(datetime.now())+"</td></tr>"
    msg = msg + "<tr><td>Tipo de Evento: </td><td>"+ 'Perdida de Señal' +"</td></tr>"
    msg = msg + "<tr><td>Activo: </td><td>+"+ 'Ref: 11 - Televisor' +"</td></tr>"
    msg = msg + "<tr><td>Descripción: </td><td>"+ "El sensor dejo de recibir señal del activo. Es posible que el activo haya dejado el inmueble" +"</td></tr>"
    msg = msg + "</table>"
    msg = msg + '<h3>Por favor ingrese a la plataforma de Domotina para gestionar este suceso.<a href="http://www.domotina.com/admin">Domotina.com</a></h3>'
    msg = msg + '<img src="http://kunagi-domotina.rhcloud.com/kunagi/kunagi.png"></html>'

    email = EmailMessage('Alarma Domotina', msg,'ing.felipe.mendivelso@gmail.com' ,['cvho31@gmail.com'])
    email.content_subtype = "html"
    email.send()