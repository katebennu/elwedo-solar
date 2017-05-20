import csv, os, requests

from datetime import datetime

from pytz import timezone

from django.core.management.base import BaseCommand

from infographics.models import Building, Apartment, ConsumptionMeasurement

from .progress_bar import show_progress

from django.db.utils import IntegrityError

import xml.etree.ElementTree as ET


class Command(BaseCommand):
    help = 'Parse and save example consumption data'

    def handle(self, *args, **options):
        self.run()
        self.stdout.write(self.style.SUCCESS('Successfully inserted dummy consumption data'))

    def run(self):
        buildings = Building.objects.all()
        apartments = Apartment.objects.all()
        utc = timezone('UTC')
        module_dir = os.path.dirname(os.path.abspath(__file__))

        with open(os.path.join(module_dir, "fixtures", 'Fregatti_short.csv')) as file:
            reader = csv.reader(file)
            rows = list(reader)
            for row in rows:
                parse_time = datetime.strptime(row[0], '%d.%m.%Y %H:%M:%S')
                try:
                    for building in buildings:
                        _, created = ConsumptionMeasurement.objects.get_or_create(
                            building=building,
                            timestamp=datetime(parse_time.year + 1, parse_time.month, parse_time.day, parse_time.hour, parse_time.minute, tzinfo=utc),
                            value=float(row[1])
                        )

                    for a in apartments:
                        _, created = ConsumptionMeasurement.objects.get_or_create(
                            apartment=a,
                            timestamp=datetime(parse_time.year + 1, parse_time.month, parse_time.day, parse_time.hour,
                                               parse_time.minute, tzinfo=utc),
                            value=float(row[1]) / float(a.building.total_area) * float(a.area)
                        )

                except IntegrityError:
                    pass

        # then request 2-week data from building servers
        base_req = """<?xml version="1.0"?>
                        <Message>
                            <Header>
                                <Verb>create</Verb>
                                <Noun>MeterReadings</Noun>
                            </Header>
                            <Payload>
                                <MeterReadings>
                                    <MeterReading>
                                        <Meter>
                                            <mRID></mRID>
                                        </Meter>
                                        <Readings>
                                            <ReadingType ref="32.26.0.0.1.1.12.0.0.0.0.0.0.0.224.3.72.0"/>
                                            <timePeriod>
                                                <end>2017-05-15T09:00:00.0000000Z</end>
                                                <start>2017-05-14T08:00:00.0000000Z</start>
                                            </timePeriod>
                                        </Readings>
                                        <valuesInterval>
                                            <end>2017-05-15T09:00:00.0000000Z</end>
                                            <start>2017-05-15T08:00:00.0000000Z</start>
                                        </valuesInterval>
                                    </MeterReading>
                                </MeterReadings>
                            </Payload>
                        </Message>"""
        req_root = ET.fromstring(base_req)

        headers = {'Content-Type': 'application/xml'}
        with open(os.path.join(module_dir, "fixtures", 'auth.csv')) as file:
            reader = csv.reader(file)
            rows = list(reader)
            for row in rows:
                auth = (row[0], row[1])

        for a in apartments:
            url = a.building.server_ip
            print(url, a.name)
            req_root.find(".//mRID").text = a.mRID
            resp = requests.get(
                url=a.building.server_ip,
                auth=auth, verify=False, headers=headers,
                data=ET.tostring(req_root))

            resp_root = ET.fromstring(resp.text)
            for reading in resp_root.findall('.//Readings'):
                value = reading.find('value').text
                parse_time = datetime.strptime(reading.find('.//end').text, '%Y-%m-%dT%H:%M:%S.0000000Z')
                _, created = ConsumptionMeasurement.objects.update_or_create(
                    apartment=a,
                    timestamp=datetime(parse_time.year + 1, parse_time.month, parse_time.day, parse_time.hour,
                                       parse_time.minute, tzinfo=utc),
                    value=float(value)
                )
                print(parse_time, created)
