import urllib.request
from datetime import datetime
from django.core.management.base import BaseCommand
from pytz import timezone
from infographics.models import ExampleGrid, ProductionMeasurement
from .progress_bar import show_progress
from django.db.utils import IntegrityError


class Command(BaseCommand):
    help = 'Parse and save example production data'

    def handle(self, *args, **options):
        self.run()
        self.stdout.write(self.style.SUCCESS('Successfully updated production data'))

    def run(self):
        url = 'https://www.helen.fi/sahko/kodit/aurinkosahko/suvilahti/DownloadData/'
        file, headers = urllib.request.urlretrieve(url)
        contents = open(file).read()
        rows = contents.splitlines()

        grid = ExampleGrid.objects.all()[0]
        tz = timezone('Europe/Helsinki')
        total_rows = len(rows)
        cursor = 0

        for i in range(800):
            row = rows[i]
            row = row.split(';')
            show_progress(cursor, total_rows)
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

                cursor += 1

            except IntegrityError:
                pass

