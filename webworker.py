from apscheduler.schedulers.background import BackgroundScheduler
from work import *
from src.models import Players
from src.models import Matches
from src.models import Practices
from src.models import AttendanceHistory
from django.contrib.admin.models import LogEntry
from axes.utils import reset

import os
import datetime

def run_web_script():
    os.system('gunicorn config.wsgi --log-file -')  # Runs forever

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(doWork, 'interval', seconds=1)
    scheduler.start()   # Runs in the 'background'

def clearEverything():
    # Delete all django-axes lockouts and access records
    reset()

    # Erase all entries in these tables
    tables = [
        Players.objects.all(),
        Matches.objects.all(),
        Practices.objects.all(),
        AttendanceHistory.objects.all(),
        LogEntry.objects.all(),
    ]

    for table in tables:
        for entry in table:
            entry.delete()

def doWork():
    '''
    We need to clear the database entries once in a while so we don't go over the row limit in the Heroku Postgres database.
    Therefore, we will reset all entries during July, since school is not in session.

    Otherwise, update the attendances and matches as usual.
    '''
    if datetime.datetime.now().month == 7:
        clearEverything()
    else:
        checkForMatchUpdates()
        checkForPracticeUpdates()
        deleteLogEntries()

def run():
    start_scheduler()
    run_web_script()




if __name__ == '__main__':
    run()
