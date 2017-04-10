import urllib.request
from datetime import datetime
from django.core.management.base import BaseCommand
from pytz import timezone
from infographics.models import Grid, ProductionMeasurement
from .progress_bar import show_progress
from apscheduler.schedulers.blocking import BlockingScheduler


class Command(BaseCommand):

    help = 'Parse and save example production data'

    sched = BlockingScheduler()

    def handle(self, *args, **options):
        print('********************************************************start execution')

        self.sched.start()

        print('Successfully updated production data')

    @sched.scheduled_job('interval', minutes=2)
    def timed_job(self):
        url = 'https://www.helen.fi/sahko/kodit/aurinkosahko/suvilahti/DownloadData/'
        file, headers = urllib.request.urlretrieve(url)
        contents = open(file).read()
        rows = contents.splitlines()

        grid = Grid.objects.all()[0]
        utc = timezone('UTC')
        total_rows = len(rows)
        cursor = 0

        for i in range(300):
            row = rows[i]
            row = row.split(';')
            show_progress(cursor, total_rows)
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

            cursor += 1









        # for i in range(20):
        #     print(i, ':', splt[i])





# temp_file = open('test.txt', 'w')


# with urllib.request.urlopen(url) as response:
#     contents = open(response[0]).read()
#     f = open('test.txt', 'w')
#     f.write(contents)
#     f.close()



# response = urllib.urlretrieve(url)
# contents = open(response[0]).read()
# f = open('filename.ext','w')
# f.write(contents)
# f.close()