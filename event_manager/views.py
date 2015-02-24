from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from .models import Event, EventType
from .serializers import EventSerializer, EventTypeSerializer

class EventViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Event.objects.all()
    serializer_class = EventSerializer

class EventTypeViewSet(viewsets.ModelViewSet):
    queryset = EventType.objects.all()
    serializer_class = EventTypeSerializer