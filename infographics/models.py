import datetime
from collections import defaultdict
from functools import partial

import pytz
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import Sum

from .utils.range import hourly, Range


def get_data_for_range(
        range_generator,
        consumption_measurement_query_set,
        building,
        place_area,
        apartment=None):
    """
    :param range_generator: function producing a set of datetime ranges, must accept a date time parameter as a limit
    :param consumption_measurement_query_set: query set of consumption values
    :param building: building object where the measurements were taken
    :param place_area: area of a given location - should be less or equal to the area of the building
    :param apartment: apartment object where the measurements were taken
    :return: generator of values
    """
    latest_consumption = consumption_measurement_query_set.order_by('-timestamp').first().timestamp
    latest_production = ProductionMeasurement.objects.order_by('-timestamp').first().timestamp

    total_capacity = building.get_target_capacity()

    for time_range in range_generator(min(latest_consumption, latest_production)):
        start = time_range.start
        end = time_range.end

        # This is a trick to make sure that the start of the range is exclusive
        actual_range = Range(start + datetime.timedelta(seconds=1), end)

        consumption_measurements = consumption_measurement_query_set.filter(timestamp__range=actual_range)
        production_measurements = ProductionMeasurement.objects.filter(timestamp__range=actual_range)

        consumption = consumption_measurements.aggregate(Sum('value'))["value__sum"]

        production = production_measurements \
                         .aggregate(Sum('percent_of_max_capacity'))[
                         "percent_of_max_capacity__sum"] * total_capacity * (place_area / building.total_area)

        # savings = min(production, consumption)

        yield {
            'timestamp': actual_range.end,
            'consumption': float(consumption),
            'production': float(production),
            # 'savings': float(savings),
            # 'consumptionLessSavings': float(consumption - savings)
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
        # day_savings = 0.0

        for result in day_results[day]:
            day_consumption += result["consumption"]
            day_production += result["production"]
            # day_savings += result["savings"]

        yield {
            'timestamp': day,
            'consumption': float(day_consumption),
            'production': float(day_production),
            # 'savings': float(day_savings),
            # 'consumptionLessSavings': float(day_consumption - day_savings)
        }


class Profile(models.Model):
    user = models.OneToOneField(User)
    apartment = models.ForeignKey('Apartment')


class Apartment(models.Model):
    name = models.fields.CharField(max_length=50)
    area = models.fields.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0.0), MaxValueValidator(999.99)], default=94.5)
    inhabitants = models.fields.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(99)], default=3)
    building = models.ForeignKey('Building')
    up_code = models.fields.IntegerField(validators=[MinValueValidator(0),
                                                     MaxValueValidator(9999999)], default=0)
    mRID = models.fields.CharField(max_length=50, default='None')

    def _get_data_estimates(self, range_generator):
        return list(get_data_for_range(
            consumption_measurement_query_set=self.consumptionmeasurement_set,
            range_generator=range_generator,
            building=self.building,
            place_area=self.area,
            apartment=self,
        ))

    def get_hour_production(self, timestamp):
        return ProductionMeasurement.objects.get(timestamp=timestamp).scale_for_apartment(self)

    def get_hour_consumption(self, timestamp):
        return ConsumptionMeasurement.objects.get(timestamp=timestamp, apartment=self).value

    def get_day_data(self, car):
        """ Returns consumption and production data for latest 24 hours that both in the database"""
        data = self._get_data_estimates(partial(hourly, 24))
        for i in data:
            if car:
                if 14 <= i['timestamp'].hour <= 18:
                    i['consumption'] += 3
            i['savings'] = float(min(i['production'], i['consumption']))
            i['consumptionLessSavings'] = float(i['consumption'] - i['savings'])
        return data

    def get_multiple_days_data(self, days, car):
        """ Returns consumption and production data for the latest N days in the database"""
        data = list(sum_for_each_day(self._get_data_estimates(partial(hourly, 24 * days))))
        for i in data:
            if car:
                i['consumption'] += 15
            i['savings'] = float(min(i['production'], i['consumption']))
            i['consumptionLessSavings'] = float(i['consumption'] - i['savings'])

        return data

    def get_grid_multiplier(self):
        return GridPriceMultiplier.objects.get(apartment=self, use=True).multiplier

    def get_solar_multiplier(self):
        return SolarPriceMultiplier.objects.get(apartment=self, use=True).multiplier

    def get_nosolar_price(self, timestamp):
        return self.get_grid_multiplier() * self.get_hour_consumption(timestamp)

    def get_withsolar_price(self, timestamp):
        g = self.get_grid_multiplier()
        s = self.get_solar_multiplier()
        c = self.get_hour_consumption(timestamp)
        p = self.get_hour_production(timestamp)
        if c > p:
            return g * (c - p) + s * p
        else:
            return s * p

    def get_building_nosolar_price(self, timestamp):
        return self.get_grid_multiplier() * self.building.get_hour_consumption(timestamp)

    def get_building_withsolar_price(self, timestamp):
        g = self.get_grid_multiplier()
        s = self.get_solar_multiplier()
        c = self.get_hour_consumption(timestamp)
        p = self.get_hour_production(timestamp)
        if c > p:
            return g * (c - p) + s * p
        else:
            return s * p


    def __str__(self):
        return str(self.building.name) + ', Apartment #' + str(self.name)


class Building(models.Model):
    name = models.fields.CharField(max_length=50, unique=True)
    total_apartments = models.fields.IntegerField(validators=[MinValueValidator(0),
                                                              MaxValueValidator(9999)], default=60)
    total_area = models.fields.DecimalField(max_digits=8,
                                            decimal_places=2,
                                            validators=[MinValueValidator(0.0),
                                                        MaxValueValidator(999999.99)], default=5238)
    total_inhabitants = models.fields.IntegerField(validators=[MinValueValidator(0),
                                                               MaxValueValidator(9999)], default=120)
    server_ip = models.fields.CharField(max_length=50)

    def get_target_capacity(self):
        return TargetCapacity.objects.get(building=self, use=True).total_capacity

    def _get_data_estimates(self, range_generator):
        return list(get_data_for_range(
            consumption_measurement_query_set=self.consumptionmeasurement_set,
            range_generator=range_generator,
            building=self,
            place_area=self.total_area
        ))

    def get_hour_production(self, timestamp):
        return ProductionMeasurement.objects.get(timestamp=timestamp).scale_for_building(self)

    def get_day_data(self, car):
        """ Returns consumption and production data for latest 24 hours that both in the database"""
        data = self._get_data_estimates(partial(hourly, 24))
        for i in data:
            if car:
                if 14 <= i['timestamp'].hour <= 18:
                    i['consumption'] += 3
            i['savings'] = float(min(i['production'], i['consumption']))
            i['consumptionLessSavings'] = float(i['consumption'] - i['savings'])
        return data

    def get_multiple_days_data(self, days, car):
        """ Returns consumption and production data for the latest N days in the database"""
        data = list(sum_for_each_day(self._get_data_estimates(partial(hourly, 24 * days))))
        for i in data:
            if car:
                i['consumption'] += 15
            i['savings'] = float(min(i['production'], i['consumption']))
            i['consumptionLessSavings'] = float(i['consumption'] - i['savings'])
        return data

    def __str__(self):
        return 'Building ' + str(self.name)


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

    def scale_for_building(self, building):
        return self.percent_of_max_capacity * building.get_target_capacity()

    def scale_for_apartment(self, apartment):
        return self.scale_for_building(apartment.building) * apartment.area / apartment.building.total_area

    def __str__(self):
        return 'Production on ' + str(self.timestamp)


class ExampleGrid(models.Model):
    name = models.fields.CharField(max_length=50, unique=True)
    # kWP
    max_capacity = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0.0), MaxValueValidator(999999.99)], default=340)

    def __str__(self):
        return 'Grid ' + str(self.name)


class TargetCapacity(models.Model):
    building = models.ForeignKey(Building)
    total_capacity = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0.0), MaxValueValidator(999999.99)], default=40)
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
    name = models.fields.CharField(max_length=50, default='default')
    multiplier = models.DecimalField(
        max_digits=8,
        decimal_places=5,
        validators=[MinValueValidator(0.0), MaxValueValidator(999.99)])
    use = models.BooleanField(default=True)


class KmMultiplier(models.Model):
    name = models.fields.CharField(max_length=50, default='default')
    multiplier = models.DecimalField(
        max_digits=8,
        decimal_places=5,
        validators=[MinValueValidator(0.0), MaxValueValidator(999.99)])
    use = models.BooleanField(default=True)


class GridPriceMultiplier(models.Model):
    name = models.fields.CharField(max_length=50, default='default')
    multiplier = models.DecimalField(
        max_digits=8,
        decimal_places=5,
        validators=[MinValueValidator(0.0), MaxValueValidator(999.99)])
    use = models.BooleanField(default=True)
    apartment = models.ForeignKey('Apartment')


class SolarPriceMultiplier(models.Model):
    name = models.fields.CharField(max_length=50, default='default')
    multiplier = models.DecimalField(
        max_digits=8,
        decimal_places=5,
        validators=[MinValueValidator(0.0), MaxValueValidator(999.99)])
    use = models.BooleanField(default=True)
    apartment = models.ForeignKey('Apartment')
