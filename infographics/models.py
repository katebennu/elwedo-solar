import datetime

from collections import defaultdict
from functools import partial

import pytz

from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import Sum

from .utils.range import hourly


def get_data_for_range(
        range_generator,
        consumption_measurement_query_set,
        building,
        apartment_divisor=1):
    """
    :param range_generator: function producing a set of datetime ranges, must accept a date time parameter as a limit
    :param consumption_measurement_query_set: query set of consumption values
    :param building: building object where the measurements were taken
    :param apartment_divisor: the number of apartments if the measurements were per apartment - 1 if for a building
    :return: generator of values
    """
    latest_consumption = consumption_measurement_query_set.order_by('-timestamp').first().timestamp
    latest_production = ProductionMeasurement.objects.order_by('-timestamp').first().timestamp

    number_of_panels = TargetCapacity.objects.filter(building=building, use=True)[0].number_of_units

    for time_range in range_generator(min(latest_consumption, latest_production)):
        consumption_measurements = consumption_measurement_query_set.filter(timestamp__range=time_range)
        production_measurements = ProductionMeasurement.objects.filter(timestamp__range=time_range)

        consumption = consumption_measurements.aggregate(Sum('value'))["value__sum"]

        production = production_measurements \
            .aggregate(Sum('value_per_unit'))["value_per_unit__sum"] * number_of_panels / apartment_divisor

        savings = production
        if production > consumption:
            savings = consumption

        yield {
            'timestamp': time_range.end,
            'consumption': float(consumption),
            'production': float(production),
            'savings': float(savings),
            'consumptionLessSavings': float(consumption - savings)
        }


def sum_for_each_day(hourly_results):

    day_results = defaultdict(list)
    for result in hourly_results:
        timestamp = result["timestamp"]
        day = datetime.datetime(
            day=timestamp.day,
            month=timestamp.month,
            year=timestamp.year,
            tzinfo=pytz.timezone("UTC"))
        day_results[day].append(result)

    for day in sorted(day_results.keys()):
        if len(day_results[day]) < 24:
            continue
        day_consumption = 0.0
        day_production = 0.0
        day_savings = 0.0

        for result in day_results[day]:
            day_consumption += result["consumption"]
            day_production += result["production"]
            day_savings += result["savings"]

        yield {
            'timestamp': day,
            'consumption': float(day_consumption),
            'production': float(day_production),
            'savings': float(day_savings),
            'consumptionLessSavings': float(day_consumption - day_savings)
        }


class Apartment(models.Model):
    name = models.fields.CharField(max_length=50, unique=True)
    area = models.fields.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0.0), MaxValueValidator(999.99)])
    inhabitants = models.fields.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(99)])
    building = models.ForeignKey('Building')
    user = models.OneToOneField(User, related_name='apartment', default=1)

    def _get_data_estimates(self, range_generator):
        return list(get_data_for_range(
            consumption_measurement_query_set=self.consumptionmeasurement_set,
            range_generator=range_generator,
            building=self.building,
            apartment_divisor=int(self.building.total_apartments)
        ))

    def get_day_data(self):
        """ Returns consumption and production data for latest 24 hours that both in the database"""
        return self._get_data_estimates(partial(hourly, 24))

    def get_multiple_days_data(self, days):
        """ Returns consumption and production data for the latest N days in the database"""
        return list(sum_for_each_day(self._get_data_estimates(partial(hourly, 24 * days))))

    def __str__(self):
        return str(self.building.address) + ', Apartment #' + str(self.number)


class Building(models.Model):
    name = models.fields.CharField(max_length=50, unique=True)
    total_apartments = models.fields.IntegerField(validators=[MinValueValidator(0),
                                                              MaxValueValidator(9999)])
    total_area = models.fields.DecimalField(max_digits=8,
                                            decimal_places=2,
                                            validators=[MinValueValidator(0.0),
                                                        MaxValueValidator(999999.99)])
    total_inhabitants = models.fields.IntegerField(validators=[MinValueValidator(0),
                                                               MaxValueValidator(9999)])

    def _get_data_estimates(self, range_generator):
        return list(get_data_for_range(
            consumption_measurement_query_set=self.consumptionmeasurement_set,
            range_generator=range_generator,
            building=self
        ))

    def get_day_data(self):
        """ Returns consumption and production data for latest 24 hours that both in the database"""
        return self._get_data_estimates(partial(hourly, 24))

    def get_multiple_days_data(self, days):
        """ Returns consumption and production data for the latest N days in the database"""
        return list(sum_for_each_day(self._get_data_estimates(partial(hourly, 24 * days))))

    def __str__(self):
        return 'Building ' + str(self.address)


class ConsumptionMeasurement(models.Model):
    # one of the two is obligatory
    apartment = models.ForeignKey(Apartment, null=True)
    building = models.ForeignKey(Building, null=True)
    timestamp = models.DateTimeField(null=True)
    value = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0.0), MaxValueValidator(999999.99)])

    class Meta:
        unique_together = (('timestamp', 'apartment'), ('timestamp', 'building'))

    def __str__(self):
        return 'Consumption on ' + str(self.timestamp)


class ProductionMeasurement(models.Model):
    timestamp = models.DateTimeField(null=True)
    # kWh / kWp
    percent_of_max_capacity = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0.0), MaxValueValidator(999999.99)])
    grid = models.ForeignKey('ExampleGrid')

    class Meta:
        unique_together = ('timestamp', 'grid')

    def __str__(self):
        return 'Production on ' + str(self.timestamp)


class ExampleGrid(models.Model):
    name = models.fields.CharField(max_length=50, unique=True)
    # kWP
    max_capacity = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0.0), MaxValueValidator(999999.99)])

    def __str__(self):
        return 'Grid ' + str(self.name)


class TargetCapacity(models.Model):
    building = models.ForeignKey(Building)
    total_capacity = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0.0), MaxValueValidator(999999.99)])
    # estimated capacity, KW, instead of units
    name = models.CharField(
        max_length=100,
        unique=True,
        default="default")
    use = models.BooleanField(default=True)

    def __str__(self):
        return str(self.total_capacity) + ' Capacity estimation, building ' + str(
            self.building.name) + ', name ' + str(self.name)


class CO2Multiplier(models.Model):
    name = models.fields.CharField(max_length=50, unique=True)
    multiplier = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0.0), MaxValueValidator(999.99)])
    use = models.BooleanField(default=True)


class KmMultiplier (models.Model):
    name = models.fields.CharField(max_length=50, unique=True)
    multiplier = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0.0), MaxValueValidator(999.99)])
    use = models.BooleanField(default=True)


class GridPriceMultiplier(models.Model):
    name = models.fields.CharField(max_length=50, unique=True)
    multiplier = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0.0), MaxValueValidator(999.99)])
    use = models.BooleanField(default=True)
    apartment = models.ForeignKey('Apartment')

class SolarPriceMultiplier(models.Model):
    name = models.fields.CharField(max_length=50, unique=True)
    multiplier = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0.0), MaxValueValidator(999.99)])
    use = models.BooleanField(default=True)
    apartment = models.ForeignKey('Apartment')