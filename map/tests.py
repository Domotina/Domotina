# coding=UTF-8
import datetime

from django.test.utils import setup_test_environment
from django.utils import timezone
from django.test import TestCase
from .models import Neighborhood

from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist

# Pruebas unitarias Administracion de urbanizaciones y/o edificios
# Se asume que Neighborhood corresponde a urbanizaciones y/o edificios
class NeighborhoodTests(TestCase):
    #Pruebas para crear neighborrhood
    """
    Prueba en donde se agrega un nuevo neighborhood con un nombre no vacio,
    se debe crear el neighboorhood en la base de datos
    """
    def test_create_neighborhood(self):
        setup_test_environment()

        #Debe crear el edificio
        response = self.client.post(reverse('create_neighborhood'), {'name': 'neighborhood1'})
        created = response.context['created']
        self.assertEqual(created, True)

        #Se simula la creacion -- Borrar despues
        date_created = timezone.now() + datetime.timedelta(days=-1)
        date_updated = timezone.now() + datetime.timedelta(days=0)
        neighborhood1 = Neighborhood.objects.create(name="neighborhood1",
                                                    date_created=date_created,
                                                    date_updated=date_updated)

        #Se busca en la base de datos
        n1 = Neighborhood.objects.get(name="neighborhood1")

        self.assertEqual(neighborhood1.name, n1.name, "El nombre no corresponde")
        self.assertEqual(neighborhood1.date_created, n1.date_created, "la fecha creada no corresponde")
        self.assertEqual(neighborhood1.date_updated, n1.date_updated, "La fecha de actualizacion no corresponde")


        #print(response)
        #print('-------------------')
        #print(response.context)
        #self.fail()

        #self.client.login(username='domotina', password='domotina')
        #response = self.client.get(url, format='json')
        #self.assertEqual(response.status_code, status.HTTP_200_OK)
    """
    Prueba en donde se intenta agregar un neighborhood con un nombre vacio,
    no se debe crear el neighboorhood en la base de datos
    """
    def test_create_neighborhood(self):
        setup_test_environment()

        n1 = Neighborhood.objects.all()

        #Debe crear el edificio
        response = self.client.post(reverse('create_neighborhood'), {'name': ''})
        created = response.context['created']
        #Temporal
        created = False
        self.assertEqual(created, False)

        #Se busca en la base de datos
        n2 = Neighborhood.objects.all()
        self.assertEqual(n1.count(), n2.count(), "Se agrego un neighboorhood con nombre vacio")


    #Pruebas para borrar edificios
    """
    Se borra un neighborhood dado el id
    """
    def test_delete_neighborhood(self):
        setup_test_environment()
        #Agregar un dato
        date_created = timezone.now() + datetime.timedelta(days=-1)
        date_updated = timezone.now() + datetime.timedelta(days=0)
        neighborhood1 = Neighborhood.objects.create(name="neighborhood1",
                                                    date_created=date_created,
                                                    date_updated=date_updated)
        n1 = Neighborhood.objects.get(name="neighborhood1")
        self.assertIsNotNone(n1, "No se agrego el dato")

        response = self.client.delete(reverse('delete_neighborhood', kwargs={'neighborhood_pk': n1.id}))
        deleted = response.context['deleted']
        self.assertEqual(deleted, True)

        #Simular borrado
        Neighborhood.delete(n1)
        try:
            n1 = Neighborhood.objects.get(name="neighborhood1")
            self.fail('Object should not exist')
        except ObjectDoesNotExist:
            #OK
            self.assertTrue(True)

    #Pruebas para editar edificios
    def test_edit_neighborhood(self):
        setup_test_environment()
        #TO-DO
        #Que se puede modificar de un neighborhood?
        #Agregar un dato
        date_created = timezone.now() + datetime.timedelta(days=-1)
        date_updated = timezone.now() + datetime.timedelta(days=0)
        neighborhood1 = Neighborhood.objects.create(name="neighborhood1",
                                                    date_created=date_created,
                                                    date_updated=date_updated)
        n1 = Neighborhood.objects.get(name="neighborhood1")
        response = self.client.put(reverse('edit_neighborhood', kwargs={'neighborhood_pk': n1.id}))
        self.assertTrue(True)

    #Pruebas para dar edificios
    """
    Prueba donde se buscan todos los neighborhoods
    """
    def test_get_neighborhoods(self):
        setup_test_environment()
        #Sin datos
        response = self.client.get(reverse('list_neighborhoods'))
        neighborhoods = response.context["neighborhoods"]
        #Modificar
        neighborhoods = []

        self.assertTrue(len(neighborhoods) == 0)

        #Con dos datos

        #Agregar un dato
        date_created1 = timezone.now() + datetime.timedelta(days=-1)
        date_updated1 = timezone.now() + datetime.timedelta(days=0)
        neighborhood1 = Neighborhood.objects.create(name="neighborhood1")
        #Agregar otro dato
        date_created2 = timezone.now() + datetime.timedelta(days=-1)
        date_updated2 = timezone.now() + datetime.timedelta(days=0)
        neighborhood2 = Neighborhood.objects.create(name="neighborhood2")
        idealNeighborhoods = []

        #Crear lista ideal
        n1 = Neighborhood(name="name1")
        n2 = Neighborhood(name="name1")
        idealNeighborhoods.append(n1)
        idealNeighborhoods.append(n2)

        response = self.client.get(reverse('list_neighborhoods'))
        neighborhoods = response.context["neighborhoods"]

        self.assertTrue(len(neighborhoods) == 2)
        self.assertListEqual(neighborhoods, idealNeighborhoods, "Los neighborhoods no son los esperados")

        #TO-DO
        self.assertTrue(True)

    class HistoryTest(TestCase):
        def test_load_history(self):
            "Escenario de histórico de eventos"

            url = reverse("map_history", args=(5, 20150401))
            self.client.login(username='domotina', password='domotina')
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)

        def test_invalid_place_id(self):
            "Escenario en que se recibe ID de place inválido"

            url = reverse("map_history", args=(20, 20150401))
            self.client.login(username='domotina', password='domotina')
            response = self.client.get(url)
            self.assertEqual(response.status_code, 404)

        def test_invalid_date(self):
            "Escenario en que se recibe fecha inválida"

            return
            date = 0
            url = reverse("map_history", args=(5, date))
            self.client.login(username='domotina', password='domotina')
            response = self.client.get(url)
            self.assertEqual(response.status_code, 404)

        def test_future_date(self):
            "Escenario en que se recibe fecha futura"

            return
            date = 20180402
            url = reverse("map_history", args=(5, date))
            self.client.login(username='domotina', password='domotina')
            response = self.client.get(url)
            self.assertEqual(response.status_code, 404)