import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'solarpilot.settings'

from apscheduler.schedulers.blocking import BlockingScheduler
from django.core.management import call_command

sched = BlockingScheduler()


@sched.scheduled_job('interval', minutes=2)
def timed_job():
    call_command('helen-data')
    print('This job is run every two minutes.')

sched.start()