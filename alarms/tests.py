from django.test import TestCase
from alarms.models import Status

class StatusTestCase(TestCase):
    def loadCases(self):
        Status.objects.create(status='active')
        Status.objects.create(status='inactive')
        Status.objects.create(status='unknown')

    def testStatus(self):
        act = Status.objects.get(status='active')
        dis = Status.objects.get(status='inactive')
        unknown = Status.objects.get(status='unknown')
        self.assertEqual(act.status,'active')
        self.assertEqual(dis.status,'inactive')
        self.assertEqual(unknown.status,'unknown')
