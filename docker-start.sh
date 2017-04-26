#!/bin/bash

cd /package
python manage.py migrate
python manage.py helen_scheduled &

chown -R www-data:www-data /mount
chown -R www-data:www-data /package
/usr/sbin/apache2ctl -D FOREGROUND
