from django.core.management.base import BaseCommand
from infographics.models import Grid, ProductionMeasurement
import csv
import os
from datetime import datetime
from pytz import timezone
import pytz


class Command(BaseCommand):
    help = 'Parse and save example production data'

    def handle(self, *args, **options):
        self.run()
        self.stdout.write(self.style.SUCCESS('Successfully inserted dummy production data'))

    def run(self):
        grid = Grid.objects.all()[0]
        utc = timezone('UTC')
        module_dir = os.path.dirname(os.path.abspath(__file__))

        with open(os.path.join(module_dir, "fixtures", 'Suvilahti_2017_March.csv')) as file:
            reader = csv.reader(file, delimiter='\t')
            for row in reader:
                try:
                    value_per_unit = float(row[1]) / grid.total_units
                except ValueError:
                    value_per_unit = 0
                parse_time = datetime.strptime(row[0], '%Y-%m-%dT%H:%M:%S')
                _, created = ProductionMeasurement.objects.get_or_create(
                    grid=grid,
                    timestamp=datetime(parse_time.year, parse_time.month, parse_time.day, parse_time.hour, parse_time.minute, tzinfo=utc),
                             value_per_unit = float(value_per_unit)
                )
