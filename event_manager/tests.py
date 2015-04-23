from rest_framework.test import APITestCase
from rest_framework import status

# Create your tests here.


class APITests(APITestCase):
    url = '/api/sensors/'

    def test_get_success(self):
        "Prueba para un GET exitoso"

        self.client.login(username='domotina', password='domotina')
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_forbidden(self):
        "Prueba para un GET fallido"

        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_put_forbidden(self):
        "Prueba para un PUT fallido"

        url = self.url + '1/'
        data = {}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_put_success(self):
        "Prueba para un PUT exitoso"

        url = self.url + '1/'
        data = {'current_value': 1}
        self.client.login(username='domotina', password='domotina')
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
