#!/bin/bash

cd /package
python manage.py migrate
chown -R www-data:www-data /mount
chown -R www-data:www-data /package
/usr/sbin/apache2ctl -D FOREGROUND
