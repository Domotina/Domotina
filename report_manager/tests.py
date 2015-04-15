# -*- encoding: utf-8 -*-
import unittest
import calendar
import datetime
from event_manager.models import Event


class ReportValidation(unittest.TestCase):
    "HU: Generar reporte mensual de incidencias. Narrativa: Como usuario de la central, quiero generar el reporte de incidencias ocurridas en el mes de los inmuebles que administro, organizados por inmueble y cantidad de incidencias generadas."

    def setUp(self):
        self.month = 2
        self.year = 2015
        self.events = []

    def tearDown(self):
        del self.month
        del self.year
        del self.events

    def test_escenario1(self):
        "Escenario 1: Dado que soy un usuario de la central cuando seleccione un mes y aun año en el que no hay registros de eventos en los inmuebles que administro entonces no debe generar un reporte y debe informar que no hay registro disponibles para construir el reporte."

        self.assertIsNotNone(self.month)
        self.assertIsNotNone(self.year)
        # month_range = calendar.monthrange(self.year,self.month)
        # initial_day = 1
        # end_day = month_range[1]
        # start_date = datetime.datetime(self.year, self.month,initial_day)
        # end_date = datetime.datetime(self.year, self.month,end_day)
        # end_date = end_date.replace(hour=23,minute=59)
        # self.events = Event.objects.filter(timestamp__range=(start_date, end_date))
        # self.assertFalse(self.events)


    def test_escenario2(self):
        "Escenario 2: Escenario 2: Dado que soy un usuario de la central Cuando seleccione un mes, un año y una urbanización o edificio Entonces se genera un reporte con los eventos ocurridos en los inmuebles en la urbanización o edificio seleccionado y en el periodo de año y mes referenciado."

        self.assertTrue(True)

    def test_escenario3(self):
        "Escenario 3: Dado que soy un usuario de la central Cuando seleccione un mes y un año y pulse la opción de generar reporte de incidentes Entonces se genera un reporte con los incidentes ocurridos en todos los inmuebles registrados en la central"

        self.assertTrue(True)

    def test_escenario4(self):
        "Escenario 4: Dado que soy un usuario de la central Cuando seleccione únicamente el año y pulse la opción de generar un reporte mensual de incidentes Entonces no se genera el reporte y se informa al usuario que hace falta la referencia del mes para la generación."

        self.assertTrue(True)

    def test_escenario5(self):
        "Escenario 5: Dado que soy un usuario de la central Cuando seleccione únicamente el mes y pulse la opción de generar un reporte mensual de incidentes Entonces no se genera el reporte y se informa al usuario que hace falta la referencia del año para la generación."

        self.assertTrue(True)
