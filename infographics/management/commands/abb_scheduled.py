from django.core.management.base import BaseCommand
import os, csv
from infographics.models import Apartment, ConsumptionMeasurement
import xml.etree.ElementTree as ET
import requests


class Command(BaseCommand):
    help = 'Parse and save real consumption data from buildings'

    def handle(self, *args, **options):
        self.run()
        self.stdout.write(self.style.SUCCESS('Successfully updated consumption data'))

    def run(self):
        module_dir = os.path.dirname(os.path.abspath(__file__))
        apartments = Apartment.objects.all()

        xml_req = """<?xml version="1.0"?>
                <Message>
                    <Header>
                        <Verb>create</Verb>
                        <Noun>MeterReadings</Noun>
                    </Header>
                    <Payload>
                        <MeterReadings>
                            <MeterReading>
                                <Meter>
                                    <mRID>08accb89-7ced-1af1-f235-d67dff5e8585</mRID>
                                </Meter>
                                <Readings>
                                    <ReadingType ref="32.26.0.0.1.1.12.0.0.0.0.0.0.0.224.3.72.0"/>
                                    <timePeriod>
                                        <end>2017-05-15T09:00:00.0000000Z</end>
                                        <start>2017-05-15T08:00:00.0000000Z</start>
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
        root = ET.fromstring(xml_req)

        headers = {'Content-Type': 'application/xml'}
        with open(os.path.join(module_dir, "fixtures", 'auth.csv')) as file:
            reader = csv.reader(file)
            rows = list(reader)
            for row in rows:
                auth = (row[0], row[1])

        for a in apartments:
            up = a.up_code
            url = a.building.server_ip + '/gc=' + str(up)
            print(url)

            root.find(".//mRID").text = a.mRID

            resp = requests.get(url=url, auth=auth, verify=False, headers=headers)
            print(resp.text)
