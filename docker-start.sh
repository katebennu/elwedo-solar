#!/bin/bash

cd /package
python manage.py migrate
python manage.py populate --verbosity 2
python manage.py add-consumption --verbosity 3
python manage.py helen_data --verbosity 3

chown -R www-data:www-data /mount
chown -R www-data:www-data /package
/usr/sbin/apache2ctl -D FOREGROUND
