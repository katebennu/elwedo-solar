import urllib.request
from datetime import datetime
from django.core.management.base import BaseCommand
from pytz import timezone
from infographics.models import ExampleGrid, ProductionMeasurement
from apscheduler.schedulers.blocking import BlockingScheduler
from django.db.utils import IntegrityError


sched = BlockingScheduler()


@sched.scheduled_job('cron', minute=20)
def timed_job():
    print('********************* started timed_job')

    url = 'https://www.helen.fi/aurinko/kodit/aurinkosahko/suvilahti/DownloadData/'
    file, headers = urllib.request.urlretrieve(url)
    contents = open(file).read()
    rows = contents.splitlines()

    print('*************** got the data')

    grid = ExampleGrid.objects.all()[0]
    tz = timezone('Europe/Helsinki')

    print('**************** got the grid')

    for i in range(50):
        row = rows[i]
        row = row.split(';')
        if 'Arvo (kWh)' in row:
            continue
        try:
            percent_of_max_capacity = float(row[1]) / float(grid.max_capacity)
        except ValueError:
            percent_of_max_capacity = 0

        parse_time = datetime.strptime(row[0], '%Y-%m-%dT%H:%M:%S')
        try:
            _, created = ProductionMeasurement.objects.get_or_create(
                grid=grid,
                timestamp=tz.localize(datetime(parse_time.year, parse_time.month, parse_time.day, parse_time.hour,
                                   parse_time.minute)),
                percent_of_max_capacity=float(percent_of_max_capacity)
            )
        except IntegrityError:
            pass
    print('*********Successfully updated production data*********')


class Command(BaseCommand):

    help = 'Parse and save example production data'

    def handle(self, *args, **options):
        print('***************************start execution')
        self.stdout.write(self.style.SUCCESS('Started updating production data'))
        sched.start()
        print('*************************** stopped')
        self.stdout.write(self.style.SUCCESS('Successfully updated production data'))

