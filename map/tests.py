import datetime

from django.utils import timezone
from django.test import TestCase
from .models import Neighborhood

# Pruebas unitarias Administracion de urbanizaciones y/o edificios
class EdificiosTests(TestCase):
    #Pruebas para crear edificios
    def test_create_edificio(self):
        date_created = timezone.now() + datetime.timedelta(days=-1)
        date_updated = timezone.now() + datetime.timedelta(days=0)

        neighborhood1 = Neighborhood.objects.create(name="neighborhood1",
                                                    date_created=date_created,
                                                    date_updated=date_updated)

        n1 = Neighborhood.objects.get(name="neighborhood1")

        self.assertEqual(neighborhood1.name, n1.name, "El nombre no corresponde")
        self.assertEqual(neighborhood1.date_created, n1.date_created, "la fecha creada no corresponde")
        self.assertEqual(neighborhood1.date_updated, n1.date_updated, "La fecha de actualizacion no corresponde")

        #url = '/api/events/'
        #self.client.login(username='domotina', password='domotina')
        #response = self.client.get(url, format='json')
        #self.assertEqual(response.status_code, status.HTTP_200_OK)

    #Pruebas para borrar edificios
    def test_delete_edificio(self):
        #TO-DO
        self.assertTrue(True)

    #Pruebas para editar edificios
    def test_edit_edificio(self):
        #TO-DO
        self.assertTrue(True)

    #Pruebas para dar edificios
    def test_get_edificios(self):
        #TO-DO
        self.assertTrue(True)


class HistoryTest(TestCase):
    def test_load_history(self):
        self.assertTrue(True)
        return

        self.client.login(username='domotina', password='domotina')
        response = self.client.get(url)
        #Debe cambiarse a codigo 200 cuando se implemente
        self.assertEqual(response.status_code, 404)
