from django.test import TestCase
from alarms.models import Status

class StatusTestCase(TestCase):
    def loadCases(self):
        Status.objects.create(status='active')
        Status.objects.create(status='inactive')

    def testStatus(self):
        act = Status.objects.get(status='active')
        dis = Status.objects.get(status='inactive')
        self.assertEqual(act.status,'active')
        self.assertEqual(dis.status,'inactive')
