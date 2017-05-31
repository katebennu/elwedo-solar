import csv, os, requests

from django.core.management.base import BaseCommand

from infographics.models import Building, Apartment, ConsumptionMeasurement

from .progress_bar import show_progress

from django.db.utils import IntegrityError

import xml.etree.ElementTree as ET


class Command(BaseCommand):
    help = 'Parse and save example consumption data'

    def handle(self, *args, **options):
        self.run()
        self.stdout.write(self.style.SUCCESS('mRIDs tested successfully'))

    def run(self):
        apartments = Apartment.objects.all()
        module_dir = os.path.dirname(os.path.abspath(__file__))

        with open(os.path.join(module_dir, "fixtures", 'auth.csv')) as file:
            reader = csv.reader(file)
            rows = list(reader)
            for row in rows:
                auth = (row[0], row[1])

        for a in apartments:

            url = a.building.server_ip
            resp = requests.get(url=url, auth=auth, verify=False)
            root = ET.fromstring(resp.text)