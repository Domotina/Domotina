from django.test import TestCase
import unittest
from django.contrib.auth.models import User
# Create your tests here.

class UserDelegate(unittest.TestCase):
    "HU Como propietario quiero delegar funciones de administracion a otras personas de forma que puedan revisar el estado de mi inmueble."
    def setUp(self):
        self.username = "pruebadelegado"
        self.name = "Prueba"
        self.lastName = "Delegado"
        self.email = "raul.gomezn@hotmail.com"
        self.password = 'DOMOTINA123'
    def tearDown(self):
        del self.username
        del self.name
        del self.lastName
        del self.email
        del self.password
    #TODO crear el nuevo grupo para delegado con sus permisos (falta)"
    """
    Escenario 1
    Dado que soy un usuario de la central
    Cuando selecciono la opcion de crear un nuevo delegado en el sistema e ingreso todos los valores requeridos
    Entonces se crea un nuevo usuario con rol delegado en el sistema.
    """
    def testStage1(self):
        userTest = User.objects.create_user(username=self.username, first_name=self.name,
                                         last_name=self.lastName, email=self.email, password=self.password)

        self.assertEqual(userTest.username, self.username)
        self.assertEqual(userTest.first_name, self.name)
        self.assertEqual(userTest.last_name, self.lastName)
        self.assertEqual(userTest.email, self.email)
        userTest.delete() #No borrar