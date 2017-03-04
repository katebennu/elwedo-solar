from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Apartment(models.Model):
    number = models.fields.IntegerField(unique=True, primary_key=True)
    area = models.fields.DecimalField(max_digits=5,
                                      decimal_places=2,
                                      validators=[MinValueValidator(0.0),
                                                  MaxValueValidator(999.99)])
    inhabitants = models.fields.IntegerField(validators=[MinValueValidator(0),
                                                         MaxValueValidator(99)])
    building = models.ForeignKey('Building')


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


# if one account per apartment, rewrite for one-to-one relation
class UserMethods(User):
    def owns_apartment(self, apartment):
        return self.apartments.filter(number=apartment.number).exists()


class ConsumptionMeasurement(models.Model):
    # one of the two is obligatory
    apartment = models.ForeignKey(Apartment, null=True)
    building = models.ForeignKey(Building, null=True)
    time = models.DateTimeField
    value = models.DecimalField(max_digits=8,
                                decimal_places=2,
                                validators=[MinValueValidator(0.0),
                                            MaxValueValidator(999999.99)])


class ProductionMeasurement(models.Model):
    time = models.DateTimeField
    value_per_unit = models.DecimalField(max_digits=8,
                                decimal_places=2,
                                validators=[MinValueValidator(0.0),
                                            MaxValueValidator(999999.99)])
    grid = models.ForeignKey('Grid')


class Grid(models.Model):
    name = models.fields.CharField(max_length=50, unique=True)
    total_units = models.fields.IntegerFieldvalidators=[MinValueValidator(0),
                                                              MaxValueValidator(999999)]