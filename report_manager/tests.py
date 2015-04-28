# -*- encoding: utf-8 -*-
import unittest
import datetime
from report_manager import central_report_gen, owner_report_gen as owner_rg
from map.models import Place


class OwnerReportTests(unittest.TestCase):

    def test_us011_scenario1(self):
        ''' Dado que soy un propietario
            Cuando seleccione un rango de fechas en el que no hay registros de eventos ocurridos en alguno de mis inmuebles
            Entonces no debe generar un reporte y debe informar que no hay registro disponibles según los datos ingresados'''

        self.start_date = "2013/01/01"
        self.end_date = "2013/01/10"
        self.place_pk = 5

        # Validating if start_date is valid
        self.assertTrue(owner_rg.is_valid_format(self.start_date))

        # Validating if end_date is valid
        self.assertTrue(owner_rg.is_valid_format(self.end_date))

        # Getting the place based on its pk
        place = owner_rg.get_place(self.place_pk)

        # Getting events in the place based on a date range
        events = owner_rg.get_events_in_place(place, self.start_date, self.end_date)

        # No events found!
        if not events or len(events) == 0:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def test_us011_scenario2(self):
        ''' Dado que soy un propietario
            Cuando seleccione un rango de fechas y hay eventos para el inmueble actual.
            Entonces se genera un reporte con los eventos ocurridos en mi inmueble detallando principalmente el activo afectado,
            cambio de estado y el momento en el que ocurrio el evento.'''

        self.start_date = "2013/01/01"
        self.end_date = "2015/12/31"
        self.place_pk = 5

        # Validating if start_date is valid
        self.assertTrue(owner_rg.is_valid_format(self.start_date))

        # Validating if end_date is valid
        self.assertTrue(owner_rg.is_valid_format(self.end_date))

        # Getting the place based on its pk
        place = owner_rg.get_place(self.place_pk)

        # Getting events in the place based on a date range
        events = owner_rg.get_events_in_place(place, self.start_date, self.end_date)

        # Events do found!
        if events and len(events) > 0:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def test_us011_scenario3(self):
        ''' Dado que soy un propietario
            Cuando seleccione unicamente la fecha inicial del rango de fechas y pulse la opción de generar reporte de eventos
            Entonces no se genera el reporte y se informa al usuario que hace falta ingresar la fecha final y el inmueble para
            la generacion.'''

        self.start_date = "2015/01/01"
        self.end_date = ""

        # Validating if start_date is valid
        self.assertTrue(owner_rg.is_valid_format(self.start_date))

        # Validating if end_date is valid
        self.assertFalse(owner_rg.is_valid_format(self.end_date))

    def test_us011_scenario4(self):
        ''' Dado que soy un propietario
            Cuando seleccione unicamente la fecha final del rango de fechas y pulse la opción de generar reporte de eventos
            Entonces no se genera el reporte y se informa al usuario que hace falta ingresar la fecha inicial y el inmueble
            para la generacion.'''

        self.start_date = ""
        self.end_date = "2015/01/20"

        # Validating if start_date is valid
        self.assertFalse(owner_rg.is_valid_format(self.start_date))

        # Validating if end_date is valid
        self.assertTrue(owner_rg.is_valid_format(self.end_date))

    def test_us011_scenario5(self):
        ''' Dado que soy un propietario
            Cuando ingreso el rango de fechas y el inmueble, pero la fecha final es menor que la fecha inicial
            Entonces no se genera el reporte y se informa al usuario que la fecha final es menor que la fecha inicial y
            por ende no se puede especificar el rango de fechas para realizar la generacion.'''

        self.start_date = "2015/01/01"
        self.end_date = "2015/01/20"

        # Validating if start_date is valid
        self.assertTrue(owner_rg.is_valid_format(self.start_date))

        # Validating if end_date is valid
        self.assertTrue(owner_rg.is_valid_format(self.end_date))

        # Validating if end date is greater than start date
        self.assertTrue(owner_rg.is_end_date_greater(self.start_date, self.end_date))



class CentralReportTests(unittest.TestCase):
    "HU: Generar reporte mensual de incidencias. Narrativa: Como usuario de la central, quiero generar el reporte de incidencias ocurridas en el mes de los inmuebles que administro, organizados por inmueble y cantidad de incidencias generadas."

    def setUp(self):
        self.month = 2
        self.year = 2000
        self.places = [1]
        self.start_date = ""
        self.end_date = ""

    def tearDown(self):
        del self.month
        del self.year
        del self.places
        del self.start_date
        del self.end_date

    def test_escenario1(self):
        "Escenario 1: Dado que soy un usuario de la central cuando seleccione un mes y aun año en el que no hay registros de eventos en los inmuebles que administro entonces no debe generar un reporte y debe informar que no hay registro disponibles para construir el reporte."

        #valida las entradas
        self.assertTrue(central_report_gen.validation_entry(self.year,self.month))
        # Ajusta fechas
        self.start_date = central_report_gen.get_start_date(self.year,self.month)
        self.end_date = central_report_gen.get_end_date(self.year,self.month)
        #busca los eventos
        events = central_report_gen.find_events(self.start_date,self.end_date,self.places)
        #Generar el report, pero dado que no hay evento, debe regresar como Falsa la creación del report.
        self.assertFalse(central_report_gen.are_events_to_report(events))

    def test_escenario2(self):
        "Escenario 2: Dado que soy un usuario de la central Cuando seleccione un mes, un año y una urbanización o edificio Entonces se genera un reporte con los eventos ocurridos en los inmuebles en la urbanización o edificio seleccionado y en el periodo de año y mes referenciado."

        #Carga la urbanización/edificio
        self.places = [4]
        self.year=2015
        self.month=4
        #valida las entradas
        self.assertTrue(central_report_gen.validation_entry(self.year,self.month))
        # Ajusta fechas
        self.start_date = central_report_gen.get_start_date(self.year,self.month)
        self.end_date = central_report_gen.get_end_date(self.year,self.month)
        #busca los eventos
        events = central_report_gen.find_events(self.start_date,self.end_date,self.places)
        #Generar el report, pero dado que no hay evento, debe regresar como Falsa la creación del report.
        self.assertTrue(central_report_gen.are_events_to_report(events))


    def test_escenario3(self):
        "Escenario 3: Dado que soy un usuario de la central Cuando seleccione un mes y un año y pulse la opción de generar reporte de incidentes Entonces se genera un reporte con los incidentes ocurridos en todos los inmuebles registrados en la central"
        #Carga la urbanización/edificio
        self.places = []
        self.year=2015
        self.month=4
        #valida las entradas
        self.assertTrue(central_report_gen.validation_entry(self.year,self.month))
        # Ajusta fechas
        self.start_date = central_report_gen.get_start_date(self.year,self.month)
        self.end_date = central_report_gen.get_end_date(self.year,self.month)
        #busca los eventos
        events = central_report_gen.find_events(self.start_date,self.end_date,self.places)
        #Generar el report, pero dado que no hay evento, debe regresar como Falsa la creación del report.
        self.assertTrue(central_report_gen.are_events_to_report(events))


    def test_escenario4(self):
        "Escenario 4: Dado que soy un usuario de la central Cuando seleccione únicamente el año y pulse la opción de generar un reporte mensual de incidentes Entonces no se genera el reporte y se informa al usuario que hace falta la referencia del mes para la generación."

        # Se ajusta a un mes inexistente
        self.month=0
        #Valida que esten todas las entradas
        self.assertFalse(central_report_gen.validation_entry(self.year,self.month))


    def test_escenario5(self):
        "Escenario 5: Dado que soy un usuario de la central Cuando seleccione únicamente el mes y pulse la opción de generar un reporte mensual de incidentes Entonces no se genera el reporte y se informa al usuario que hace falta la referencia del año para la generación."

        # Se ajusta a un mes inexistente
        self.year=0
        #Valida que esten todas las entradas
        self.assertFalse(central_report_gen.validation_entry(self.year,self.month))