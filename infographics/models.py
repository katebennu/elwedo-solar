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
        """ Returns consumption and production data for latest 24 hours in the database"""
        # get latest timestamps

        # compare timestamps and find out which is the earliest of the two


        # retrieve consumption for 24 hours before that timestamp

        pass

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

# if one account per apartment, rewrite for one-to-one relation
class UserMethods(User):
    def owns_apartment(self, apartment):
        return self.apartments.filter(number=apartment.number).exists()


class ConsumptionMeasurement(models.Model):
    # one of the two is obligatory
    apartment = models.ForeignKey(Apartment, null=True)
    building = models.ForeignKey(Building, null=True)
    timestamp = models.DateTimeField(null=True)
    value = models.DecimalField(max_digits=8,
                                decimal_places=2,
                                validators=[MinValueValidator(0.0),
                                            MaxValueValidator(999999.99)])


class ProductionMeasurement(models.Model):
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