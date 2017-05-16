import csv, os

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

from infographics.models import *

from .progress_bar import show_progress

User = get_user_model()
from pprint import pprint

class Command(BaseCommand):
    help = 'Create apartment objects for a building'

    def handle(self, *args, **options):
        self.run()
        self.stdout.write(self.style.SUCCESS('Successfully inserted dummy base data'))

    def run(self):
        fregatti, created = Building.objects.get_or_create(
            name='Fregatti',
            total_apartments=60,
            total_area=5238,
            total_inhabitants=120,
        )

        fiskari, created = Building.objects.get_or_create(
            name='Fiskari',
            total_apartments=60,
            total_area=5238,
            total_inhabitants=120,
        )

        TargetCapacity.objects.get_or_create(
            building=fiskari,
            total_capacity=100,
            name='fiskari from populator'
        )

        TargetCapacity.objects.get_or_create(
            building=fregatti,
            total_capacity=100,
            name='fregatti from populator'
        )
        module_dir = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(module_dir, "fixtures", 'apartments.csv')) as file:
            reader = csv.reader(file)
            rows = list(reader)
            for row in rows:
                pprint(row)
                building = Building.objects.get(name=row[4])
                a = Apartment(name=row[0], area=row[2], inhabitants=row[3], building=building)
                a.save()
                pprint(a.name)
                g, _ = GridPriceMultiplier.objects.get_or_create(name='grid price from populator ' + a.name, multiplier=0.12, apartment=a)
                s, _ = SolarPriceMultiplier.objects.get_or_create(name='solar price from populator ' + a.name, multiplier=0.06, apartment=a)
                pprint(g.name)
                pprint(s.name)
                for i in range(2):
                    username = row[0] + '_user_' + str(i + 1)
                    u, _ = User.objects.get_or_create(username=username)
                    u.set_password('pass')
                    u.save()
                    Profile.objects.get_or_create(user=u, apartment=a)

        ExampleGrid.objects.get_or_create(name='Suvilahti', max_capacity=300)

        CO2Multiplier.objects.get_or_create(name='co2 from populator', multiplier=0.21)
        KmMultiplier.objects.get_or_create(name='km from populator', multiplier=5)

