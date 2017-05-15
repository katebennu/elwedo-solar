# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-13 19:16
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Apartment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('area', models.DecimalField(decimal_places=2, max_digits=5, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(999.99)])),
                ('inhabitants', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(99)])),
            ],
        ),
        migrations.CreateModel(
            name='Building',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('total_apartments', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(9999)])),
                ('total_area', models.DecimalField(decimal_places=2, max_digits=8, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(999999.99)])),
                ('total_inhabitants', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(9999)])),
            ],
        ),
        migrations.CreateModel(
            name='CO2Multiplier',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('multiplier', models.DecimalField(decimal_places=2, max_digits=8, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(999.99)])),
                ('use', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='ConsumptionMeasurement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(null=True)),
                ('value', models.DecimalField(decimal_places=2, max_digits=8, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(999999.99)])),
                ('apartment', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='infographics.Apartment')),
                ('building', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='infographics.Building')),
            ],
        ),
        migrations.CreateModel(
            name='ExampleGrid',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('max_capacity', models.DecimalField(decimal_places=2, max_digits=8, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(999999.99)])),
            ],
        ),
        migrations.CreateModel(
            name='GridPriceMultiplier',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('multiplier', models.DecimalField(decimal_places=2, max_digits=8, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(999.99)])),
                ('use', models.BooleanField(default=True)),
                ('apartment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='infographics.Apartment')),
            ],
        ),
        migrations.CreateModel(
            name='KmMultiplier',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('multiplier', models.DecimalField(decimal_places=2, max_digits=8, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(999.99)])),
                ('use', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProductionMeasurement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(null=True)),
                ('percent_of_max_capacity', models.DecimalField(decimal_places=2, max_digits=8, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(999999.99)])),
                ('grid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='infographics.ExampleGrid')),
            ],
        ),
        migrations.CreateModel(
            name='SolarPriceMultiplier',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('multiplier', models.DecimalField(decimal_places=2, max_digits=8, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(999.99)])),
                ('use', models.BooleanField(default=True)),
                ('apartment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='infographics.Apartment')),
            ],
        ),
        migrations.CreateModel(
            name='TargetCapacity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_capacity', models.DecimalField(decimal_places=2, max_digits=8, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(999999.99)])),
                ('name', models.CharField(default='default', max_length=100, unique=True)),
                ('use', models.BooleanField(default=True)),
                ('building', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='infographics.Building')),
            ],
        ),
        migrations.AddField(
            model_name='apartment',
            name='building',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='infographics.Building'),
        ),
        migrations.AlterUniqueTogether(
            name='productionmeasurement',
            unique_together=set([('timestamp', 'grid')]),
        ),
        migrations.AlterUniqueTogether(
            name='consumptionmeasurement',
            unique_together=set([('timestamp', 'building'), ('timestamp', 'apartment')]),
        ),
    ]
