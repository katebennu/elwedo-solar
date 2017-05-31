import csv, os

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

from infographics.models import *

from .progress_bar import show_progress

User = get_user_model()

class Command(BaseCommand):
    help = 'Create apartment objects for a building'

    def handle(self, *args, **options):
        self.run()
        self.stdout.write(self.style.SUCCESS('Successfully inserted dummy base data'))

    def run(self):
        module_dir = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(module_dir, "fixtures", 'buildings.csv')) as file:
            reader = csv.reader(file)
            rows = list(reader)
            for row in rows:
                building, created = Building.objects.get_or_create(
                    name=row[0],
                    total_apartments=row[3],
                    total_area=row[1],
                    total_inhabitants=row[4],
                    server_ip=row[2]
                )

                TargetCapacity.objects.get_or_create(
                    building=building,
                    total_capacity=40,
                    name= building.name + ' from populator'
                )

        with open(os.path.join(module_dir, "fixtures", 'apartments.csv')) as file:
            reader = csv.reader(file)
            rows = list(reader)
            for row in rows:
                building = Building.objects.get(name=row[4])
                a = Apartment(
                    name=row[0],
                    area=row[2],
                    inhabitants=row[3],
                    up_code=row[6],
                    mRID=row[7],
                    building=building)
                a.save()
                g, _ = GridPriceMultiplier.objects.get_or_create(name='grid price from populator ' + a.name, multiplier=0.12, apartment=a)
                s, _ = SolarPriceMultiplier.objects.get_or_create(name='solar price from populator ' + a.name, multiplier=0.06, apartment=a)
                for i in range(2):
                    if row[0] == 'Guest':
                        if i == 0:
                            username = 'Guest'
                        else:
                            username = 'Vieras'
                    else:
                        username = row[0] + '_user_' + str(i + 1)
                    u, _ = User.objects.get_or_create(username=username)
                    u.set_password(row[8+i])
                    u.save()
                    Profile.objects.get_or_create(user=u, apartment=a)

        ExampleGrid.objects.get_or_create(name='Suvilahti', max_capacity=340)

        CO2Multiplier.objects.get_or_create(name='co2 from populator', multiplier=0.21)
        KmMultiplier.objects.get_or_create(name='km from populator', multiplier=5)

