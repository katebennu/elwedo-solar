# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-31 17:26

from django.db import migrations
from django.contrib.auth.models import User
from django.conf import settings


USERNAME = "admin"
PASSWORD = "admin"


def create_superuser(apps, schema_editor):
    if not settings.DEBUG:
        return
    User.objects.create_superuser(
        username=USERNAME, password=PASSWORD, email='x@x.com')


class Migration(migrations.Migration):

    dependencies = [('infographics', '0010_auto_20170329_1237'),]

    operations = [migrations.RunPython(create_superuser)]