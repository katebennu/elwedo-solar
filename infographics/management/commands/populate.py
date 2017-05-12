import csv, os

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

from infographics.models import Building, Apartment, ExampleGrid, TargetCapacity

from .progress_bar import show_progress

User = get_user_model()


class Command(BaseCommand):
    help = 'Create apartment objects for a building'

    def handle(self, *args, **options):
        self.run()
        self.stdout.write(self.style.SUCCESS('Successfully inserted dummy base data'))

    def run(self):
        fregatti, created = Building.objects.get_or_create(
            address='Fregatti',
            total_apartments=60,
            total_area=5238,
            total_inhabitants=120,
        )

        fiskari, created = Building.objects.get_or_create(
            address='Fiskari',
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
                building = Building.objects.get(name=row[4])
                a = Apartment(name=row[0], area=row[2], inhabitants=row[3], building=building)
                a.save()
                for i in range(2):
                    username = row[0] + str(i + 1)
                    password = row[0]
                    u, _ = User.objects.get_or_create(username=username, is_active=True)
                    u.set_password(password)
                    u.save()



    ExampleGrid.objects.get_or_create(name='Suvilahti', total_units=194)
