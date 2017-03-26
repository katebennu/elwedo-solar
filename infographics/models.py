from django.db import models
from django.db.models.functions import Trunc
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import datetime, timedelta


class Apartment(models.Model):
    def __str__(self):
        return str(self.building.address) + ', Apartment #' + str(self.number)

    number = models.fields.IntegerField(unique=True, primary_key=True)
    area = models.fields.DecimalField(max_digits=5,
                                      decimal_places=2,
                                      validators=[MinValueValidator(0.0),
                                                  MaxValueValidator(999.99)])
    inhabitants = models.fields.IntegerField(validators=[MinValueValidator(0),
                                                         MaxValueValidator(99)])
    building = models.ForeignKey('Building')


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
        return max(latest_consumption, latest_production)

    def get_day_data(self):
        """ Returns consumption and production data for latest 24 hours that both in the database"""
        latest = self.get_latest_time()
        earliest = latest - timedelta(days=1)


        # retrieve consumption for 24 hours before that timestamp
        result_consumption = list(
            self.consumptionmeasurement_set.filter(timestamp__range=[earliest, latest]))
        result_production = list(
            ProductionMeasurement.objects.filter(timestamp__range=[earliest, latest]))
        return {'consumption': result_consumption, 'production': result_production}

    def get_week_data(self):
        #
        # """ Returns consumption and production data for latest 7 days in the database"""
        # latest = self.get_latest_time()
        # # get date of week ago to get the range (to get only needed results in query,
        # # because splitted query cannot be filtered later and has to be made again)
        # earliest = latest - timedelta(days=7)
        #
        #
        #
        #
        #
        #
        #
        # # retrieve consumption for 7 days before that timestamp
        # result_consumption = self.consumptionmeasurement_set.exclude(timestamp__gt=latest).order_by('-timestamp')[:192]
        # # add annotation day
        # annotate_days = result_consumption.annotate(day=Trunc('timestamp', 'day', output_field=models.DateTimeField()))
        # # get a set of days
        # days_list = list(set([i.day for i in annotate_days]))
        # days_list.sort()
        # # get total for each day in set
        # for d in days_list:
        #     annotate_days.filter(timestamp__day=d.day)
        #
        #
        #
        # result_production = list(
        #     ProductionMeasurement.objects.exclude(timestamp__gt=latest).order_by('-timestamp')[:24])
        #return {'consumption': result_consumption, 'production': result_production}
        pass

    def get_month_data(self):
        """ Returns consumption and production data for latest 30 days in the database"""
        # get latest timestamps

        # compare timestamps and find out which is the earliest of the two


        # retrieve consumption for 30 days before that timestamp

        pass


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


class Grid(models.Model):
    def __str__(self):
        return 'Grid ' + str(self.name)

    name = models.fields.CharField(max_length=50, unique=True)
    total_units = models.fields.IntegerField(default=200)
