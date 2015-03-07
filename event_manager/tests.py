from django.test import TestCase

from event_manager.models import EventType, Event, Alarm
from django.utils import timezone

# Create your tests here.

class SimpleEventTest(TestCase):
    def test_EventType__unicode(self):
        """
        Test EventType.__unicode__()
        """
        tName = "eventName"
        tDescription = "eventDescription"
        tCritical = False
        eventType = EventType(name=tName, description=tDescription, is_critical=tCritical)
        
        self.assertEqual(eventType.__unicode__(), tName)

#    def test_Event_unicode(self):
#        """
#        Test EventType.__unicode__()
#        """
#        tName = "eventName"
#        tDescription = "eventDescription"
#        tCritical = False
#        eventType = EventType(name=tName, description=tDescription, is_critical=tCritical)
#        
#        time = timezone.now()
#        event = Event(sensor = None, type=eventType, timeStamp = time, pos_x=1, pos_y=1)
#
#        event = Event(sensor = null, )
#        alarm = Alarm()
#        future_question = Question(pub_date=time)
#        self.assertEqual(future_question.was_published_recently(), False)


