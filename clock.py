import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'solarpilot.settings'

from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()


@sched.scheduled_job('interval', minutes=2)
def timed_job():


    print('This job is run every two minutes.')

sched.start()