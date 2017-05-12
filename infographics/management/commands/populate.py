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
            total_area=3000,
            total_inhabitants=120,
        )

        fiskari, created = Building.objects.get_or_create(
            address='Fiskari',
            total_apartments=60,
            total_area=3000,
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

        with open(os.path.join(module_dir, "fixtures", 'Fregatti_short.csv')) as file:
            reader = csv.reader(file)
            rows = list(reader)
            total_rows = len(rows)
            cursor = 0
            for row in rows:

        for n in range(total_apartments):
            show_progress(n, total_apartments)
            username = 'user_' + str(n + 1)
            password = 'pass_' + str(n + 1)
            u, _ = User.objects.get_or_create(username=username, is_active=True)
            u.set_password(password)
            u.save()
            a = Apartment(number=n + 1, area=area, inhabitants=inhabitants, building=building, user=u)
            a.save()

        ExampleGrid.objects.get_or_create(name='Suvilahti', total_units=194)

