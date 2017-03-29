from django.db import models
from django.db.models import Sum
from django.db.models.functions import Trunc
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import datetime, timedelta


class Apartment(models.Model):
    def __str__(self):
        return str(self.building.address) + ', Apartment #' + str(self.number)

    number = models.fields.IntegerField(unique=True, primary_key=True, validators=[MinValueValidator(0),
                                                                                   MaxValueValidator(9999)])
    area = models.fields.DecimalField(max_digits=5,
                                      decimal_places=2,
                                      validators=[MinValueValidator(0.0),
                                                  MaxValueValidator(999.99)])
    inhabitants = models.fields.IntegerField(validators=[MinValueValidator(0),
                                                         MaxValueValidator(99)])
    building = models.ForeignKey('Building')
    user = models.OneToOneField(User, related_name='apartment', default=1)

    def get_latest_time(self):
        # get latest timestamps
        latest_consumption = self.consumptionmeasurement_set.order_by('-timestamp').first().timestamp
        latest_production = ProductionMeasurement.objects.order_by('-timestamp').first().timestamp
        # compare timestamps and find out which is the earliest of the two
        return min(latest_consumption, latest_production)

    def query_consumption(self, earliest, latest):
        return self.consumptionmeasurement_set.filter(timestamp__range=[earliest, latest])

    def get_panels_estimate(self):
        return PanelsToInstall.objects.filter(building=self, use=True)[0].number_of_units

    def get_day_data(self):
        """ Returns consumption and production data for latest 24 hours that both in the database"""
        latest = self.get_latest_time()
        earliest = latest - timedelta(hours=23)
        q_consumption = self.query_consumption(earliest, latest)
        q_production = query_production(earliest, latest)

        panels = self.get_panels_estimate()

        result = []
        for i in q_consumption:
            production = q_production.filter(timestamp=i.timestamp)[0].value_per_unit * panels
            savings = i.value - production
            if savings < 0:
                savings = i.value
            earnings = production - i.value
            if earnings < 0:
                earnings = 0
            result.append({
                'timestamp': i.timestamp,
                'consumption': i.value,
                'production': production,
                'savings': savings,
                'consumptionLessSavings': i.value - savings,
                'earnings': earnings})
        return result

    def get_multiple_days_data(self, days):
        """ Returns consumption and production data for the latest N days in the database"""
        latest = self.get_latest_time()
        earliest = (latest - timedelta(days=days)).replace(hour=0)
        q_consumption = self.query_consumption(earliest, latest)
        q_production = query_production(earliest, latest)
        # add annotation day
        consumption_by_days = q_consumption.annotate(day=Trunc('timestamp', 'day', output_field=models.DateTimeField()))
        production_by_days = q_production.annotate(day=Trunc('timestamp', 'day', output_field=models.DateTimeField()))
        # get a set of days
        days_list = list(set([i.day for i in consumption_by_days]))
        days_list.sort()

        panels = self.get_panels_estimate()

        result = []
        for d in days_list:
            consumption_value = consumption_by_days.filter(timestamp__day=d.day).aggregate(Sum('value'))
            production_value = production_by_days.filter(timestamp__day=d.day).aggregate(Sum('value_per_unit'))
            consumption = consumption_value['value__sum']
            production = production_value['value_per_unit__sum'] * panels

            savings = consumption - production
            if savings < 0:
                savings = consumption
            earnings = production - consumption
            if earnings < 0:
                earnings = 0

            result.append({'timestamp': d,
                           'consumption': consumption,
                           'production': production,
                           'savings': savings,
                           'consumptionLessSavings': consumption - savings,
                           'earnings': earnings
                           })
        return result


class Building(models.Model):
    def __str__(self):
        return 'Building ' + str(self.address)

    address = models.fields.CharField(max_length=50, unique=True)
    total_apartments = models.fields.IntegerField(validators=[MinValueValidator(0),
                                                              MaxValueValidator(9999)])
    total_area = models.fields.DecimalField(max_digits=8,
                                            decimal_places=2,
                                            validators=[MinValueValidator(0.0),
                                                        MaxValueValidator(999999.99)])
    total_inhabitants = models.fields.IntegerField(validators=[MinValueValidator(0),
                                                               MaxValueValidator(9999)])

    def get_latest_time(self):
        # get latest timestamps
        latest_consumption = self.consumptionmeasurement_set.order_by('-timestamp').first().timestamp
        latest_production = ProductionMeasurement.objects.order_by('-timestamp').first().timestamp
        # compare timestamps and find out which is the earliest of the two
        return min(latest_consumption, latest_production)

    def query_consumption(self, earliest, latest):
        return self.consumptionmeasurement_set.filter(timestamp__range=[earliest, latest])

    def get_panels_estimate(self):
        return PanelsToInstall.objects.filter(building=self, use=True)[0].number_of_units

    def get_day_data(self):
        """ Returns consumption and production data for latest 24 hours that both in the database"""
        latest = self.get_latest_time()
        earliest = latest - timedelta(hours=23)
        q_consumption = self.query_consumption(earliest, latest)
        q_production = query_production(earliest, latest)

        panels = self.get_panels_estimate()

        result = []
        for i in q_consumption:
            production = q_production.filter(timestamp=i.timestamp)[0].value_per_unit * panels
            savings = i.value - production
            if savings < 0:
                savings = i.value
            earnings = production - i.value
            if earnings < 0:
                earnings = 0
            result.append({
                'timestamp': i.timestamp,
                'consumption': i.value,
                'production': production,
                'savings': savings,
                'consumptionLessSavings': i.value - savings,
                'earnings': earnings})
        return result

    def get_multiple_days_data(self, days):
        """ Returns consumption and production data for the latest N days in the database"""
        latest = self.get_latest_time()
        earliest = (latest - timedelta(days=days)).replace(hour=0)
        q_consumption = self.query_consumption(earliest, latest)
        q_production = query_production(earliest, latest)
        # add annotation day
        consumption_by_days = q_consumption.annotate(day=Trunc('timestamp', 'day', output_field=models.DateTimeField()))
        production_by_days = q_production.annotate(day=Trunc('timestamp', 'day', output_field=models.DateTimeField()))
        # get a set of days
        days_list = list(set([i.day for i in consumption_by_days]))
        days_list.sort()

        panels = self.get_panels_estimate()

        result = []
        for d in days_list:
            consumption_value = consumption_by_days.filter(timestamp__day=d.day).aggregate(Sum('value'))
            production_value = production_by_days.filter(timestamp__day=d.day).aggregate(Sum('value_per_unit'))
            consumption = consumption_value['value__sum']
            production = production_value['value_per_unit__sum'] * panels

            savings = consumption - production
            if savings < 0:
                savings = consumption
            earnings = production - consumption
            if earnings < 0:
                earnings = 0

            result.append({'timestamp': d,
                           'consumption': consumption,
                           'production': production,
                           'savings': savings,
                           'consumptionLessSavings': consumption - savings,
                           'earnings': earnings
                           })
        return result


class PanelsToInstall(models.Model):
    def __str__(self):
        return str(self.number_of_units) + ' Panels estimation, building ' + str(
            self.building.address) + ', name ' + str(self.name)

    building = models.ForeignKey(Building)
    number_of_units = models.IntegerField(validators=[MinValueValidator(0),
                                                      MaxValueValidator(999999)])
    name = models.CharField(max_length=100, unique=True, default="default")
    use = models.BooleanField(default=True)


# if one account per apartment, rewrite for one-to-one relation
class UserMethods(User):
    def owns_apartment(self, apartment):
        """ Determine if user owns the apartment"""
        return self.apartments.filter(number=apartment.number).exists()


class ConsumptionMeasurement(models.Model):
    def __str__(self):
        return 'Consumption on ' + str(self.timestamp)

    # one of the two is obligatory
    apartment = models.ForeignKey(Apartment, null=True)
    building = models.ForeignKey(Building, null=True)
    timestamp = models.DateTimeField(null=True)
    value = models.DecimalField(max_digits=8,
                                decimal_places=2,
                                validators=[MinValueValidator(0.0),
                                            MaxValueValidator(999999.99)])


class ProductionMeasurement(models.Model):
    def __str__(self):
        return 'Production on ' + str(self.timestamp)

    timestamp = models.DateTimeField(null=True)
    value_per_unit = models.DecimalField(max_digits=8,
                                         decimal_places=2,
                                         validators=[MinValueValidator(0.0),
                                                     MaxValueValidator(999999.99)])
    grid = models.ForeignKey('Grid')


def query_production(earliest, latest):
    return ProductionMeasurement.objects.filter(timestamp__range=[earliest, latest])


class Grid(models.Model):
    def __str__(self):
        return 'Grid ' + str(self.name)

    name = models.fields.CharField(max_length=50, unique=True)
    total_units = models.fields.IntegerField(default=200)
