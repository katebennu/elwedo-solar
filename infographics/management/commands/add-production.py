from django.core.management.base import BaseCommand
from infographics.models import ExampleGrid, ProductionMeasurement
import csv
import os
from datetime import datetime
from pytz import timezone
from django.db.utils import IntegrityError


from .progress_bar import show_progress


class Command(BaseCommand):
    help = 'Parse and save example production data'

    def handle(self, *args, **options):
        self.run()
        self.stdout.write(self.style.SUCCESS('Successfully inserted dummy production data'))

    def run(self):
        grid = ExampleGrid.objects.all()[0]
        utc = timezone('UTC')
        module_dir = os.path.dirname(os.path.abspath(__file__))

        with open(os.path.join(module_dir, "fixtures", 'production_tiny.csv')) as file:
            reader = csv.reader(file, delimiter=',')
            rows = list(reader)
            total_rows = len(rows)
            cursor = 0
            for row in rows:
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

                try:
                    _, created = ProductionMeasurement.objects.get_or_create(
                        grid=grid,
                        timestamp=datetime(parse_time.year, parse_time.month, parse_time.day, parse_time.hour, parse_time.minute, tzinfo=utc),
                                 value_per_unit = float(value_per_unit)
                    )

                    cursor += 1
                except IntegrityError:
                    pass
