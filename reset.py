import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

django.setup()

from src.models import Players
from src.models import Matches
from src.models import Practices
from src.models import AttendanceHistory
from django.contrib.admin.models import LogEntry
from axes.utils import reset

response = raw_input("Are you sure you want to reset the current entries for Players, Matches, Practices, and Attendance? (Y/N) ")

if response.upper() != 'Y':
    print "Reset aborted."
else:
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

    print "Reset complete."


