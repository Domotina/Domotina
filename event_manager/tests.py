from django.test import TestCase
from event_manager.models import EventType
from rest_framework.test import APITestCase
from rest_framework import status

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


class APITests(APITestCase):
    fixtures = ['test_fx.json']
    def test_get_success(self):
        url = '/api/events/'
        self.client.login(username='domotina', password='domotina')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    def test_get_forbidden(self):
        url = '/api/events/'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    def test_post_forbidden(self):
        url = '/api/events/'
        data = {}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.login(username='domotina', password='domotina')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    def test_post_success(self):
        url = '/api/events/'
        data = {'type': 1, 'sensor': 1}
        self.client.login(username='domotina', password='domotina')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)