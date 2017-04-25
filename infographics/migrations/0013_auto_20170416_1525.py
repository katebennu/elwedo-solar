# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-16 15:25
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('infographics', '0012_usermethods_fix'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='consumptionmeasurement',
            unique_together=set([('timestamp', 'apartment'), ('timestamp', 'building')]),
        ),
        migrations.AlterUniqueTogether(
            name='productionmeasurement',
            unique_together=set([('timestamp', 'grid')]),
        ),
    ]