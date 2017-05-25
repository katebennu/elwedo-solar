from django.test import TestCase
from infographics.models import *
from datetime import datetime

class DataTestCase (TestCase):
    def setUp(self):
        b = Building.objects.create(name='Test Building')
        a = Apartment.objects.create(name='Test Apartment', building=b)
        g = ExampleGrid.objects.create(name='Test Grid', max_capacity=340)
        ConsumptionMeasurement.objects.create(timestamp=datetime(2017, 5, 21, 9),
                                              building=b,
                                              value=23.94)
        ProductionMeasurement.objects.create(timestamp=datetime(2017, 5, 21, 9),
                                              grid=g,
                                              value=104)

        # test that production scales to building correctly
        

        # test that production is allocated to apartment correctly


        # test that spendings withot solar energy are calculated correctly


        # test that spending with account for solar energy is calulated correctly