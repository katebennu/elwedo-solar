from django.core.management.base import BaseCommand
from infographics.models import Building, ConsumptionMeasurement

class Command(BaseCommand):
    help = 'Parse and save example consumption data'

    def handle(self, *args, **options):
        self.run()
        self.stdout.write(self.style.SUCCESS('Successfully inserted dummy data'))

    def run(self):
        # building = Building.objects.all()[0]
        #
        # with
        #
        # measurement =

        pass