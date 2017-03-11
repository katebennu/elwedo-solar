from django.core.management.base import BaseCommand
from infographics.models import Building, ConsumptionMeasurement
import csv
import os
from django.utils.dateparse import parse_datetime
from dateutil.parser import parse


class Command(BaseCommand):
    help = 'Parse and save example consumption data'

    def handle(self, *args, **options):
        self.run()
        self.stdout.write(self.style.SUCCESS('Successfully inserted dummy consumption data'))

    def run(self):
        building = Building.objects.all()[0]

        module_dir = os.path.dirname(os.path.abspath(__file__))

        with open(os.path.join(module_dir, "fixtures", 'Fregatti_2016.csv')) as file:
            reader = csv.reader(file)
            for row in reader:
                _, created = ConsumptionMeasurement.objects.get_or_create(
                    building=building,
                    time=parse(row[0]),
                    value=row[1]
                )
