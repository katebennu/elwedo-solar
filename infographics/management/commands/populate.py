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


        building, created = Building.objects.get_or_create(
            address='Fregatti',
            total_apartments=60,
            total_area=3000,
            total_inhabitants=120,
        )

        TargetCapacity.objects.get_or_create(
            building=building,
            number_of_units=100,
            name='from populator'
        )

        total_apartments = building.total_apartments
        total_area = building.total_area
        total_inhabitants = building.total_inhabitants

        area = round(total_area / total_apartments)
        inhabitants = round(total_inhabitants / total_apartments)

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

