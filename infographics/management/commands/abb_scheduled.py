import csv
import os
import requests
import xml.etree.ElementTree as ET
from datetime import datetime
from datetime import timedelta

from apscheduler.schedulers.blocking import BlockingScheduler
from django.core.management.base import BaseCommand
from pytz import timezone

from infographics.models import Apartment, ConsumptionMeasurement

sched = BlockingScheduler()


@sched.scheduled_job('cron', minute=25)
def timed_job():
    print('********************* started timed_job')

    apartments = Apartment.objects.all()
    utc = timezone('UTC')
    module_dir = os.path.dirname(os.path.abspath(__file__))

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

    end = datetime.now().replace(minute=0, second=0, microsecond=0)
    start = end - timedelta(days=13)

    req_root.find('.//Readings').find('.//end').text = end.isoformat() + '.0000000Z'
    req_root.find('.//Readings').find('.//start').text = start.isoformat() + '.0000000Z'

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
        print(ET.tostring(req_root))
        resp = requests.get(
            url=a.building.server_ip,
            auth=auth, verify=False, headers=headers,
            data=ET.tostring(req_root))

        resp_root = ET.fromstring(resp.text)
        for reading in resp_root.findall('.//Readings'):
            value = reading.find('value').text
            parse_time = datetime.strptime(reading.find('.//end').text, '%Y-%m-%dT%H:%M:%S.0000000Z')
            try:
                ConsumptionMeasurement.objects.get(
                    apartment=a,
                    timestamp=datetime(parse_time.year, parse_time.month, parse_time.day, parse_time.hour,
                                       parse_time.minute, tzinfo=utc),
                ).delete()
            except ConsumptionMeasurement.DoesNotExist:
                pass
            _, created = ConsumptionMeasurement.objects.update_or_create(
                apartment=a,
                timestamp=datetime(parse_time.year, parse_time.month, parse_time.day, parse_time.hour,
                                   parse_time.minute, tzinfo=utc),
                value=float(value)
            )
            print(parse_time, created)

    print('*********Successfully updated consumption data*********')


class Command(BaseCommand):

    help = 'Parse and save example consumption data'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Started listening to house servers'))
        self.run()
        self.stdout.write(self.style.SUCCESS('Successfully inserted real consumption data'))




