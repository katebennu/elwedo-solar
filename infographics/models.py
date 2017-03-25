from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


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

    def get_day_data(self):
        """ Returns consumption and production data for latest 24 hours that both in the database"""
        # get latest timestamps
        latest_consumption = self.consumptionmeasurement_set.order_by('-timestamp').first().timestamp
        latest_production = ProductionMeasurement.objects.order_by('-timestamp').first().timestamp
        # compare timestamps and find out which is the earliest of the two
        latest = max(latest_consumption, latest_production)

        # retrieve consumption for 24 hours before that timestamp

        result_consumption = list(self.consumptionmeasurement_set.exclude(timestamp__gt=latest).order_by('-timestamp')[:24])
        result_production = list(ProductionMeasurement.objects.exclude(timestamp__gt=latest).order_by('-timestamp')[:24])
        return {'consumption': result_consumption, 'production': result_production}

    def get_week_data(self):
        """ Returns consumption and production data for latest 7 days in the database"""
        # get latest timestamps

        # compare timestamps and find out which is the earliest of the two


        # retrieve consumption for 7 days before that timestamp

        pass

    def get_month_data(self):
        """ Returns consumption and production data for latest 30 days in the database"""
        # get latest timestamps

        # compare timestamps and find out which is the earliest of the two


        # retrieve consumption for 30 days before that timestamp

        pass


class PanelsToInstall(models.Model):
    def __str__(self):
        return str(self.number_of_units) + ' Panels estimation for building ' + str(self.building.address)
    building = models.ForeignKey(Building)
    number_of_units = models.IntegerField(validators=[MinValueValidator(0),
                                                              MaxValueValidator(999999)])


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