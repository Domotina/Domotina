# -*- encoding: utf-8 -*-
import unittest
from report_manager import central_report_gen
from map.models import Place

class CentralReportTests(unittest.TestCase):
    "HU: Generar reporte mensual de incidencias. Narrativa: Como usuario de la central, quiero generar el reporte de incidencias ocurridas en el mes de los inmuebles que administro, organizados por inmueble y cantidad de incidencias generadas."

    def setUp(self):
        self.month = 2
        self.year = 2015
        self.places = []

    def tearDown(self):
        del self.month
        del self.year
        del self.places

    def test_escenario1(self):
        "Escenario 1: Dado que soy un usuario de la central cuando seleccione un mes y aun año en el que no hay registros de eventos en los inmuebles que administro entonces no debe generar un reporte y debe informar que no hay registro disponibles para construir el reporte."

        #valida las entradas
        self.assertTrue(central_report_gen.validation_entry(self.year,self.month,self.places))
        #busca los eventos
        events = central_report_gen.find_events(self.year,self.month,self.places)
        #Generar el report, pero dado que no hay evento, debe regresar como Falsa la creación del report.
        self.assertFalse(central_report_gen.generate_report(events))

    def test_escenario2(self):
        "Escenario 2: Dado que soy un usuario de la central Cuando seleccione un mes, un año y una urbanización o edificio Entonces se genera un reporte con los eventos ocurridos en los inmuebles en la urbanización o edificio seleccionado y en el periodo de año y mes referenciado."

        #Carga la urbanización/edificio
        self.places = Place.objects.get(pk=1)
        #valida las entradas
        self.assertTrue(central_report_gen.validation_entry(self.year,self.month,self.places))
        #busca los eventos
        events = central_report_gen.find_events(self.year,self.month,self.places)
        #Generar el report, pero dado que no hay evento, debe regresar como Falsa la creación del report.
        self.assertTrue(central_report_gen.generate_report(events))


    def test_escenario3(self):
        "Escenario 3: Dado que soy un usuario de la central Cuando seleccione un mes y un año y pulse la opción de generar reporte de incidentes Entonces se genera un reporte con los incidentes ocurridos en todos los inmuebles registrados en la central"
        #Carga la urbanización/edificio
        self.places = [1]
        #valida las entradas
        self.assertTrue(central_report_gen.validation_entry(self.year,self.month,self.places))
        #busca los eventos
        events = central_report_gen.find_events(self.year,self.month,self.places)
        #Generar el report, pero dado que no hay evento, debe regresar como Falsa la creación del report.
        self.assertTrue(central_report_gen.generate_report(events))


    def test_escenario4(self):
        "Escenario 4: Dado que soy un usuario de la central Cuando seleccione únicamente el año y pulse la opción de generar un reporte mensual de incidentes Entonces no se genera el reporte y se informa al usuario que hace falta la referencia del mes para la generación."

        # Se ajusta a un mes inexistente
        self.month=0
        #Valida que esten todas las entradas
        self.assertFalse(central_report_gen.validation_entry(self.year,self.month,self.places))


    def test_escenario5(self):
        "Escenario 5: Dado que soy un usuario de la central Cuando seleccione únicamente el mes y pulse la opción de generar un reporte mensual de incidentes Entonces no se genera el reporte y se informa al usuario que hace falta la referencia del año para la generación."

        # Se ajusta a un mes inexistente
        self.year=0
        #Valida que esten todas las entradas
        self.assertFalse(central_report_gen.validation_entry(self.year,self.month,self.places))