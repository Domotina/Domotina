from django.contrib import admin
from django.conf import settings
from django import forms
from forms import PlaceForm
from models import Building, Place, Device, Door, Window

admin.site.register(Building)
admin.site.register(Place)
admin.site.register(Door)
admin.site.register(Window)
admin.site.register(Device)