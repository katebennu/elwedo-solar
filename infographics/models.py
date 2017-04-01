from functools import partial

from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import Sum

from .utils.range import daily, hourly


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

    number_of_panels = PanelsToInstall.objects.get(building=building, use=True).number_of_units

    for time_range in range_generator(lambda: min(latest_consumption, latest_production)):
        consumption_measurements = consumption_measurement_query_set.filter(timestamp__range=time_range)
        production_measurements = ProductionMeasurement.objects.filter(timestamp__range=time_range)

        consumption = consumption_measurements.aggregate(Sum('value'))["value__sum"]

        production = production_measurements \
            .aggregate(Sum('value_per_unit'))["value_per_unit__sum"] * number_of_panels / apartment_divisor

        savings = consumption - production
        if savings < 0:
            savings = consumption
        earnings = production - consumption
        if earnings < 0:
            earnings = 0

        yield {
            'timestamp': time_range.end,
            'consumption': float(consumption),
            'production': float(production),
            'savings': float(savings),
            'consumptionLessSavings': float(consumption - savings),
            'earnings': float(earnings)
        }


class Apartment(models.Model):
    number = models.fields.IntegerField(
        unique=True,
        primary_key=True,
        validators=[MinValueValidator(0), MaxValueValidator(9999)])
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
            apartment_divisor=self.building.total_apartments
        ))

    def get_day_data(self):
        """ Returns consumption and production data for latest 24 hours that both in the database"""
        return self._get_data_estimates(partial(hourly, 24))

    def get_multiple_days_data(self, days):
        """ Returns consumption and production data for the latest N days in the database"""
        return self._get_data_estimates(partial(daily, days))

    def __str__(self):
        return str(self.building.address) + ', Apartment #' + str(self.number)


class Building(models.Model):
    address = models.fields.CharField(max_length=50, unique=True)
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
        return self._get_data_estimates(partial(daily, days))

    def __str__(self):
        return 'Building ' + str(self.address)


class PanelsToInstall(models.Model):
    building = models.ForeignKey(Building)
    number_of_units = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(999999)])
    name = models.CharField(
        max_length=100,
        unique=True,
        default="default")
    use = models.BooleanField(default=True)

    def __str__(self):
        return str(self.number_of_units) + ' Panels estimation, building ' + str(
            self.building.address) + ', name ' + str(self.name)


# if one account per apartment, rewrite for one-to-one relation
class UserMethods(User):

    def owns_apartment(self, apartment):
        """ Determine if user owns the apartment"""
        return self.apartments.filter(number=apartment.number).exists()


class ConsumptionMeasurement(models.Model):
    # one of the two is obligatory
    apartment = models.ForeignKey(Apartment, null=True)
    building = models.ForeignKey(Building, null=True)
    timestamp = models.DateTimeField(null=True)
    value = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0.0), MaxValueValidator(999999.99)])

    def __str__(self):
        return 'Consumption on ' + str(self.timestamp)


class ProductionMeasurement(models.Model):
    timestamp = models.DateTimeField(null=True)
    value_per_unit = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0.0), MaxValueValidator(999999.99)])
    grid = models.ForeignKey('Grid')

    def __str__(self):
        return 'Production on ' + str(self.timestamp)


class Grid(models.Model):
    name = models.fields.CharField(max_length=50, unique=True)
    total_units = models.fields.IntegerField(default=200)

    def __str__(self):
        return 'Grid ' + str(self.name)
