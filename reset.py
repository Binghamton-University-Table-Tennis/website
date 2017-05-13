import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

django.setup()

from src.models import Players
from src.models import Matches
from src.models import Practices
from src.models import AttendanceHistory

response = raw_input("Are you sure you want to reset the current entries for Players, Matches, Practices, and Attendance? (Y/N) ")

if response.upper() != 'Y':
    print "Reset aborted."
else:
    # Erase all entries in these tables
    tables = [
        Players.objects.all(),
        Matches.objects.all(),
        Practices.objects.all(),
        AttendanceHistory.objects.all(),
    ]

    for table in tables:
        for entry in table:
            entry.delete()

    print "Reset complete."


