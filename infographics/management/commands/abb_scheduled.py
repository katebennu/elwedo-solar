from django.core.management.base import BaseCommand
import os, csv
from infographics.models import Apartment, ConsumptionMeasurement
import requests


class Command(BaseCommand):
    help = 'Parse and save real consumption data from buildings'

    def handle(self, *args, **options):
        self.run()
        self.stdout.write(self.style.SUCCESS('Successfully updated consumption data'))

    def run(self):
        module_dir = os.path.dirname(os.path.abspath(__file__))
        apartments = Apartment.objects.all()

        headers = {'Content-Type': 'application/xml'}
        with open(os.path.join(module_dir, "fixtures", 'auth.csv')) as file:
            reader = csv.reader(file)
            rows=list(reader)
            for row in rows:
                auth = (row[0],row[1])

            for a in apartments:
                up = a.up_code
                url = a.building.server_ip + '/gc=' + str(up)
                print(url)
                resp = requests.get(url=url, auth=auth, verify=False)
                print(resp.text)


