from django.test import TestCase
from infographics.models import *
from datetime import datetime
from pytz import timezone


class DataTestCase(TestCase):
    def setUp(self):
        b = Building.objects.create(name='Test Building')
        TargetCapacity.objects.create(building=b)
        a = Apartment.objects.create(name='Test Apartment', building=b)
        g = ExampleGrid.objects.create(name='Test Grid', max_capacity=340)

        tz = timezone('Europe/Helsinki')
        t = datetime(2017, 5, 21, 9)

        ConsumptionMeasurement.objects.create(timestamp=tz.localize(t),
                                              building=b,
                                              value=23.94)
        ConsumptionMeasurement.objects.create(timestamp=datetime(2017, 5, 21, 6, tzinfo=timezone('UTC')),
                                              apartment=a,
                                              value=0.12)
        ProductionMeasurement.objects.create(timestamp=tz.localize(t),
                                             grid=g,
                                             percent_of_max_capacity=104/g.max_capacity)

    # test that timestamps from servers with UTC time and from other sources with local Helsinki time are synchronised
    def test_timezones(self):
        b = Building.objects.get(name='Test Building')
        a = Apartment.objects.get(name='Test Apartment')
        ca = ConsumptionMeasurement.objects.get(apartment=a).timestamp
        cb = ConsumptionMeasurement.objects.get(building=b).timestamp
        print(ca)
        self.assertEqual(ca, cb)

    # test that production scales to building correctly
    def test_production_scaling_to_building(self):
        b = Building.objects.get(name='Test Building')
        g = ExampleGrid.objects.get(name='Test Grid')
        p = ProductionMeasurement.objects.get(grid=g)
        t = TargetCapacity.objects.get(building=b)
        self.assertEqual(round(p.percent_of_max_capacity * t.total_capacity), round(12.24))

    # test that production is allocated to apartment correctly
    # def test_production_allocation_to_apartment(self):
    #     a = Apartment.objects.get(name='Test Apartment')
    #     pass

    # test that spendings withot solar energy are calculated correctly


    # test that spending with account for solar energy is calulated correctly


# LATER: test that
