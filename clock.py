import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'solarpilot.settings'

from apscheduler.schedulers.blocking import BlockingScheduler
from django.core.management import call_command
import urllib.request

sched = BlockingScheduler()


@sched.scheduled_job('interval', minutes=2)
def timed_job():
    # utils.helen_data()
    url = 'https://www.helen.fi/sahko/kodit/aurinkosahko/suvilahti/DownloadData/'
    file, headers = urllib.request.urlretrieve(url)
    contents = open(file).read()
    rows = contents.splitlines()
    print(rows[:10])

sched.start()