# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-11 19:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('infographics', '0004_productionmeasurement_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='grid',
            name='total_units',
            field=models.IntegerField(default=200),
        ),
    ]