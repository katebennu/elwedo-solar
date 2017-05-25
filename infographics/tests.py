from django.test import TestCase
from infographics.models import *
from datetime import datetime


class DataTestCase(TestCase):
    def setUp(self):
        b = Building.objects.create(name='Test Building')
        TargetCapacity.objects.create(building=b)
        a = Apartment.objects.create(name='Test Apartment', building=b)
        g = ExampleGrid.objects.create(name='Test Grid', max_capacity=340)
        ConsumptionMeasurement.objects.create(timestamp=datetime(2017, 5, 21, 9),
                                              building=b,
                                              value=23.94)
        ConsumptionMeasurement.objects.create(timestamp=datetime(2017, 5, 21, 9),
                                              apartment=a,
                                              value=0.12)
        ProductionMeasurement.objects.create(timestamp=datetime(2017, 5, 21, 9),
                                             grid=g,
                                             percent_of_max_capacity=104/g.max_capacity)

    # test that production scales to building correctly
    def test_production_scales_to_building(self):
        b = Building.objects.get(name='Test Building')
        g = ExampleGrid.objects.get(name='Test Grid')
        p = ProductionMeasurement.objects.get(timestamp=datetime(2017, 5, 21, 9),
                                              grid=g)
        t = TargetCapacity.objects.get(building=b)
        self.assertEqual(round(p.percent_of_max_capacity * t.total_capacity), round(12.24))

    # test that production is allocated to apartment correctly


    # test that spendings withot solar energy are calculated correctly


    # test that spending with account for solar energy is calulated correctly
