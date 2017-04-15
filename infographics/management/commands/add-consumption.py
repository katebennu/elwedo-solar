import csv, os

from datetime import datetime

from pytz import timezone

from django.core.management.base import BaseCommand

from infographics.models import Building, Apartment, ConsumptionMeasurement

from .progress_bar import show_progress


class Command(BaseCommand):
    help = 'Parse and save example consumption data'

    def handle(self, *args, **options):
        self.run()
        self.stdout.write(self.style.SUCCESS('Successfully inserted dummy consumption data'))

    def run(self):
        building = Building.objects.all()[0]
        apartments = Apartment.objects.order_by('number')[:5]
        rates = [0.7, 0.88, 1.1, 1.21, 1.3]
        utc = timezone('UTC')
        module_dir = os.path.dirname(os.path.abspath(__file__))

        with open(os.path.join(module_dir, "fixtures", 'Fregatti_short.csv')) as file:
            reader = csv.reader(file)
            rows = list(reader)
            total_rows = len(rows)
            cursor = 0
            for row in rows:
                show_progress(cursor, total_rows)

                parse_time = datetime.strptime(row[0], '%d.%m.%Y %H:%M:%S')
                _, created = ConsumptionMeasurement.objects.get_or_create(
                    building=building,
                    timestamp=datetime(parse_time.year + 1, parse_time.month, parse_time.day, parse_time.hour, parse_time.minute, tzinfo=utc),
                    value=float(row[1])
                )

                for a, r in zip(apartments, rates):
                    _, created = ConsumptionMeasurement.objects.get_or_create(
                        apartment=a,
                        timestamp=datetime(parse_time.year + 1, parse_time.month, parse_time.day, parse_time.hour,
                                           parse_time.minute, tzinfo=utc),
                        value=float(row[1]) / building.total_apartments * r
                    )
                cursor += 1
