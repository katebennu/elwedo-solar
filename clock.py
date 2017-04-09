import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'solarpilot.settings'

import urllib.request
from datetime import datetime

from apscheduler.schedulers.background import BackgroundScheduler
from pytz import timezone

from infographics.models import Grid, ProductionMeasurement

sched = BackgroundScheduler()


@sched.scheduled_job('interval', minutes=2)
def timed_job():
    url = 'https://www.helen.fi/sahko/kodit/aurinkosahko/suvilahti/DownloadData/'
    file, headers = urllib.request.urlretrieve(url)
    contents = open(file).read()
    rows = contents.splitlines()

    grid = Grid.objects.all()[0]
    utc = timezone('UTC')

    for i in range(300):
        row = rows[i]
        row = row.split(';')
        if 'Arvo (kWh)' in row:
            continue
        try:
            value_per_unit = float(row[1]) / grid.total_units
        except ValueError:
            value_per_unit = 0
        # except IndexError:
        #     continue
        parse_time = datetime.strptime(row[0], '%Y-%m-%dT%H:%M:%S')
        _, created = ProductionMeasurement.objects.get_or_create(
            grid=grid,
            timestamp=datetime(parse_time.year, parse_time.month, parse_time.day, parse_time.hour,
                               parse_time.minute, tzinfo=utc),
            value_per_unit=float(value_per_unit)
        )

    print('This job is run every two minutes.')

sched.start()