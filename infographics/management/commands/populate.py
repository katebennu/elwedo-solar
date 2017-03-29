from django.core.management.base import BaseCommand
from infographics.models import Building, Apartment, Grid
from django.contrib.auth.models import User


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

        total_apartments = building.total_apartments
        total_area = building.total_area
        total_inhabitants = building.total_inhabitants

        area = round(total_area / total_apartments)
        inhabitants = round(total_inhabitants / total_apartments)
        for n in range(total_apartments):
            username = 'user_' + str(n + 1)
            password = 'pass_' + str(n + 1)
            u = User(username=username)
            u.set_password(password)
            a = Apartment(number=n + 1, area=area, inhabitants=inhabitants, building=building, user=u)
            a.save()
            u.save()

        Grid.objects.get_or_create(name='Suvilahti', total_units=194)

