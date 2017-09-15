from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from apscheduler.schedulers.background import BackgroundScheduler
from work import *
import os

def run_web_script():
    os.system('gunicorn config.wsgi --log-file -')  # Runs forever

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(doWork, 'interval', seconds=1)
    scheduler.start()   # Runs in the 'background'

def doWork():
    checkForMatchUpdates()
    checkForPracticeUpdates()
    deleteLogEntries()

def run():
    start_scheduler()
    run_web_script()


if __name__ == '__main__':
    run()
