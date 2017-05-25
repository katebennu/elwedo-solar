from django.test import TestCase
from infographics.models import *
from datetime import datetime
from pytz import timezone


class DataTestCase(TestCase):
    def setUp(self):
        b = Building.objects.create(name='Test Building', total_area=5238)
        TargetCapacity.objects.create(building=b)
        a = Apartment.objects.create(name='Test Apartment', building=b, area=94.5)
        g = ExampleGrid.objects.create(name='Test Grid', max_capacity=340)

        GridPriceMultiplier.objects.create(apartment=a, multiplier=0.12)
        SolarPriceMultiplier.objects.create(apartment=a, multiplier=0.06)

        tz = timezone('Europe/Helsinki')
        t = datetime(2017, 5, 21, 9)

        ConsumptionMeasurement.objects.create(timestamp=tz.localize(t),
                                              building=b,
                                              value=23.94)
        ConsumptionMeasurement.objects.create(timestamp=datetime(2017, 5, 21, 6, tzinfo=timezone('UTC')),
                                              apartment=a,
                                              value=0.13)
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
        t = TargetCapacity.objects.get(building=b)
        time = timezone('Europe/Helsinki').localize(datetime(2017, 5, 21, 9))
        self.assertEqual(round(b.get_hour_production(time)), round(12.24))

    # test that production is allocated to apartment correctly
    def test_production_allocation_to_apartment(self):
        a = Apartment.objects.get(name='Test Apartment')
        time = timezone('Europe/Helsinki').localize(datetime(2017, 5, 21, 9))
        self.assertEqual(round(float(a.get_hour_production(time)), 2), 0.22)

    # test that spendings withot solar energy are calculated correctly
    def test_without_solar_calculation(self):
        # for apartment
        a = Apartment.objects.get(name='Test Apartment')
        time = timezone('Europe/Helsinki').localize(datetime(2017, 5, 21, 9))
        self.assertEqual(round(float(a.get_nosolar_price_one_hour(time)), 3), 0.016)


        # and for building


    # test that spending with account for solar energy is calulated correctly
    # for building


    # and for apartment


