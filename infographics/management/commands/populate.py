from django.core.management.base import BaseCommand
from infographics.models import Building, Apartment, Grid


building = Building.objects.all()[0]
total_apartments = building.total_apartments
total_area = building.total_area
total_inhabitants = building.total_inhabitants


class Command(BaseCommand):
    help = 'Create apartment objects for a building'

    def handle(self, *args, **options):
        self.run()
        self.stdout.write(self.style.SUCCESS('Successfully inserted dummy data'))

    def run(self):
        building



        area = round(total_area / total_apartments)
        inhabitants = round(total_inhabitants / total_apartments)

        for n in range(total_apartments):
            Apartment.objects.create(number=n+1, area=area, inhabitants=inhabitants, building=building)


