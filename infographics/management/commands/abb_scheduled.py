import os, csv
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Parse and save real consumption data from buildings'

    def handle(self, *args, **options):
        self.run()
        self.stdout.write(self.style.SUCCESS('Successfully updated consumption data'))

    def run(self):
        module_dir = os.path.dirname(os.path.abspath(__file__))

        with open(os.path.join(module_dir, "fixtures", 'auth.csv')) as file:
            reader = csv.reader(file)
            rows=list(reader)
            for row in rows:
                auth = (row[0],row[1])
            print(auth)

