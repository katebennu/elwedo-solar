from apscheduler.schedulers.blocking import BlockingScheduler
from django.core.management import call_command

sched = BlockingScheduler()


@sched.scheduled_job('interval', minutes=3)
def timed_job():
    call_command('heroku run python manage.py helen-data')
    print('This job is run every three minutes.')

sched.start()