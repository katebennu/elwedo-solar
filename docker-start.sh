#!/bin/bash

cd /package
python manage.py migrate
python manage.py populate
python manage.py add-consumption
python manage.py add-production

chown -R www-data:www-data /mount
chown -R www-data:www-data /package
/usr/sbin/apache2ctl -D FOREGROUND
