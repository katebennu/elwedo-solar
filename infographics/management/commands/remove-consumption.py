from django.core.management.base import BaseCommand

from infographics.models import Building, Apartment, ConsumptionMeasurement


class Command(BaseCommand):
    help = 'Parse and save example consumption data'

    def handle(self, *args, **options):
        self.run()
        self.stdout.write(self.style.SUCCESS('Successfully removed all consumption data'))

    def run(self):
        ConsumptionMeasurement.objects.all().delete()
