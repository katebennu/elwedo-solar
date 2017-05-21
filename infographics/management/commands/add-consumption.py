import csv, os, requests

from datetime import datetime, timedelta

from pytz import timezone

from django.core.management.base import BaseCommand

from infographics.models import Building, Apartment, ConsumptionMeasurement

from .progress_bar import show_progress

from django.db.utils import IntegrityError

import xml.etree.ElementTree as ET


class Command(BaseCommand):
    help = 'Parse and save example consumption data'

    def handle(self, *args, **options):
        self.run()
        self.stdout.write(self.style.SUCCESS('Successfully inserted dummy consumption data'))

    def run(self):
        buildings = Building.objects.all()
        apartments = Apartment.objects.all()
        utc = timezone('UTC')
        module_dir = os.path.dirname(os.path.abspath(__file__))

        with open(os.path.join(module_dir, "fixtures", 'Fregatti_short.csv')) as file:
            reader = csv.reader(file)
            rows = list(reader)
            for row in rows:
                parse_time = datetime.strptime(row[0], '%d.%m.%Y %H:%M:%S')
                try:
                    for building in buildings:
                        _, created = ConsumptionMeasurement.objects.get_or_create(
                            building=building,
                            timestamp=datetime(parse_time.year + 1, parse_time.month, parse_time.day, parse_time.hour, parse_time.minute, tzinfo=utc),
                            value=float(row[1])
                        )

                    for a in apartments:
                        _, created = ConsumptionMeasurement.objects.get_or_create(
                            apartment=a,
                            timestamp=datetime(parse_time.year + 1, parse_time.month, parse_time.day, parse_time.hour,
                                               parse_time.minute, tzinfo=utc),
                            value=float(row[1]) / float(a.building.total_area) * float(a.area)
                        )

                except IntegrityError:
                    pass



