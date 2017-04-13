import urllib.request
from datetime import datetime
from django.core.management.base import BaseCommand
from pytz import timezone
from infographics.models import Grid, ProductionMeasurement
from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()


@sched.scheduled_job('cron', minute=20)
def timed_job():
    print('********************* started timed_job')

    url = 'https://www.helen.fi/sahko/kodit/aurinkosahko/suvilahti/DownloadData/'
    file, headers = urllib.request.urlretrieve(url)
    contents = open(file).read()
    rows = contents.splitlines()

    print('*************** got the data')

    grid = Grid.objects.all()[0]
    utc = timezone('UTC')

    print('**************** got the grid')

    for i in range(50):
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
    print('*********Successfully updated production data*********')


class Command(BaseCommand):

    help = 'Parse and save example production data'

    def handle(self, *args, **options):
        print('***************************start execution')
        sched.start()