from django.test import TestCase
import unittest
from django.contrib.auth.models import User
from map.models import Place
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404
# Create your tests here.

class UserDelegate(unittest.TestCase):
    "HU Como propietario quiero delegar funciones de administracion a otras personas de forma que puedan revisar el estado de mi inmueble."
    error_occured = False

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
        userTest.is_superuser = False
        userTest.is_active = True
        userTest.is_staff = False
        #userTest.groups.add()
        self.assertEqual(userTest.username, self.username)
        self.assertEqual(userTest.first_name, self.name)
        self.assertEqual(userTest.last_name, self.lastName)
        self.assertEqual(userTest.email, self.email)
        userTest.delete() #No borrar
    """
    Escenario 2
    Dado que soy un usuario de la central
    Cuando voy a crear un nuevo delegado en el sistema e ingreso unicamente el nombre del usuario
    Entonces no se crea el nuevo usuario con rol delegado y se saca un mensaje en el cual se pida el ingreso de los valores requeridos.
    """
    def testStage2(self):
        userTest = User.objects.create_user(username=self.username)
        userTest.is_superuser = False
        userTest.is_active = True
        userTest.is_staff = False
        #userTest.groups.add()
        self.assertEqual(userTest.username, self.username)

        userTest.delete() #No borrar
    """
    Escenario 3
    Dado que soy un usuario de la central
    Cuando voy a crear un nuevo delegado en el sistema e ingreso unicamente el apellido del usuario
    Entonces no se crea el nuevo usuario con rol delegado y se saca un mensaje en el cual se pida el ingreso de los valores requeridos.
    """
    def testStage3(self):
        try:
            userTest = User.objects.create_user(last_name=self.lastName)
            userTest.is_superuser = False
            userTest.is_active = True
            userTest.is_staff = False
            #userTest.groups.add()
            self.error_occured = False
            userTest.delete()
        except:
            self.error_occured = True

        self.assertTrue(self.error_occured == True)

    """
    Escenario 4
    Dado que soy un usuario de la central
    Cuando voy a crear un nuevo delegado en el sistema y selecciono unicamente el propietario
    Entonces no se crea el nuevo usuario con rol delegado y se saca un mensaje en el cual se pida el ingreso de los valores requeridos.
    """
    def testStage4(self):
        try:
             user = User.objects.get(username='user') #propietario
             userTest = User.objects.create_user()
             userTest.is_superuser = False
             userTest.is_active = True
             userTest.is_staff = False
             #userTest.groups.add()

             self.error_occured = False
        except:
             self.error_occured = True

        self.assertTrue(self.error_occured == True)
        """
        Escenario 5
        Dado que soy un usuario de la central
        Cuando voy a crear un nuevo delegado en el sistema y selecciono unicamente el inmueble para el que va a ser delegado
        Entonces no se crea el nuevo usuario con rol delegado y se saca un mensaje en el cual se pida el ingreso de los valores requeridos.
        """
    def testStage5(self):
        try:
             place = Place.objects.get(name='Salitre City') #inmueble
             userTest = User.objects.create_user(username='')
             userTest.is_superuser = False
             userTest.is_active = True
             userTest.is_staff = False
             #userTest.groups.add()

             self.error_occured = False
        except:
             self.error_occured = True

        self.assertTrue(self.error_occured == True)
        """
        Escenario 6
        Dado que soy un propietario
        Cuando voy a configurar los permisos que va a tener un delegado en mi inmueble y seleccione el tipo de informacion que deseo revise
        Entonces se asignan los permisos de acceso seleccionados y se remueven los permisos no seleccionados a la informacion al usuario con rol delegado seleccionado.
        """
    def testStage6(self):
        userTest = User.objects.create_user(username=self.username, first_name=self.name,
                                         last_name=self.lastName, email=self.email, password=self.password)
        userTest.is_superuser = False
        userTest.is_active = True
        userTest.is_staff = False
        #userTest.groups.add()

        content_type = ContentType.objects.get_for_model(Place)
        permission = Permission.objects.get(content_type=content_type, codename='add_place')

        userTest.user_permissions.add(permission)
        userTest.save()
        self.assertEqual(userTest.username, self.username)
        self.assertEqual(userTest.first_name, self.name)
        self.assertEqual(userTest.last_name, self.lastName)
        self.assertEqual(userTest.email, self.email)
        # Request new instance of User
        user = get_object_or_404(User, pk=userTest.pk)
        self.assertTrue(user.has_perm('map.add_place') == True)
        userTest.delete() #No borrar
        """
        Escenario 7
        Dado que soy un propietario
        Cuando voy a configurar los permisos que va a tener un delegado en mi inmueble y no selecciono el delegado
        Entonces no se asignan los permisos y se solicita seleccionar un delegado.
        """
    def testStage7(self):
        try:
            user = User.objects.get(username='')
            content_type = ContentType.objects.get_for_model(Place)
            permission = Permission.objects.get(content_type=content_type, codename='add_place')
            #user.groups.add()
            place = Place.objects.get(name='Salitre City') #inmueble
            self.error_occured = False
        except:
            self.error_occured = True

        self.assertTrue(self.error_occured == True)
        """
        Escenario 8
        Dado que soy un delegado
        Cuando ingreso por URL, una direccion a la cual no tengo permisos
        Entonces no se debe mostrar la informacion de esta URL ingresada.
        """
    def testStage8(self):
        user = User.objects.get(username='buildersmart')
        content_type = ContentType.objects.get_for_model(Place)
        permission = Permission.objects.get(content_type=content_type, codename='add_place')

        self.assertTrue(user.has_perm('map.add_place') == False)

        """
        Escenario 9
        Dado que soy un delegado
        Cuando ingreso por URL, una direccion a la cual tengo permisos
        Entonces se debe mostrar la informacion de esta URL ingresada.
        """
    def testStage9(self):
        user = User.objects.get(username='domotina')
        content_type = ContentType.objects.get_for_model(Place)
        permission = Permission.objects.get(content_type=content_type, codename='add_place')

        self.assertTrue(user.has_perm('map.add_place') == True)