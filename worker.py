import django
import os
import time
from datetime import date
import datetime
from dst import is_dst
from django.utils import timezone
import pytz

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

django.setup()

from src.models import Greeting
from src.models import Players
from src.models import Matches
from src.models import ClubAttendance
from src.models import Practices
from src.models import AttendanceHistory

from src.Ratings import *


def checkForUpdates():

    #we extract all matches that haven't been put towards players' ratings, and sort them by the date the matches occurred
    notYetUpdated = Matches.objects.all().filter(Updated = 0).order_by('Day')
    #iterating over each match, we update the stats of the winner and loser for that match
    for m in notYetUpdated:
        winner = Players.objects.all().filter(First_Name__iexact = m.Winner_First_Name, Last_Name__iexact = m.Winner_Last_Name)
        loser = Players.objects.all().filter(First_Name__iexact = m.Loser_First_Name, Last_Name__iexact = m.Loser_Last_Name)
        win = 0
        lose = 0
        winPts = []

        for w, l in zip(winner, loser):

            # Delete entry if winner and loser are the same person
            if w.First_Name.title() == l.First_Name.title() and w.Last_Name.title() == l.Last_Name.title():
                m.delete()
                break

            win = w.Rating
            lose = l.Rating
            #call function that calculates how much the players' ratings should change, based on their difference in skill level
            # Returns array: [Winner's new rating, Loser's new rating, Points exchanged]
            winPts = calculateRatings(win, lose)

            winnerMatchesPlayed = w.Matches_Played + 1
            loserMatchesPlayed = l.Matches_Played + 1
            winnerMatchesWon = w.Matches_Won + 1
            loserMatchesWon = l.Matches_Won

            w.Rating = winPts[0]
            l.Rating = winPts[1]

            w.Matches_Played += 1
            l.Matches_Played += 1

            w.Matches_Won += 1
            l.Matches_Lost += 1

            # Calculate win rate percentage- need to use floats to force floating point arithmetic
            w.Win_Rate = int((float(winnerMatchesWon) / winnerMatchesPlayed)*100)
            l.Win_Rate = int((float(loserMatchesWon) / loserMatchesPlayed)*100)

            # Mark player as having played this week (+10 points per week)
            #w.Played_This_Week = 1
            #l.Played_This_Week = 1

            w.save()
            l.save()

        if len(winPts) != 0:
            m.Points = winPts[2]
            m.Winner_Rating = winPts[0]
            m.Loser_Rating = winPts[1]
            m.Updated = 1
            m.save()

def checkAttendance():
    attendees = ClubAttendance.objects.all()
    hadPractice = False
    attendance_count = 0

    for attendee in attendees:

        # Check for duplicate attendance entries
        duplicateAttendee = ClubAttendance.objects.all().filter(First_Name__iexact = attendee.First_Name, Last_Name__iexact = attendee.Last_Name)

        if duplicateAttendee.count() > 1:
            attendee.delete()
            continue

        # Check for existing entry for this attendee in attendance history for today
        duplicateAttendanceEntry = AttendanceHistory.objects.all().filter(First_Name__iexact = attendee.First_Name, Last_Name__iexact = attendee.Last_Name, Date = datetime.datetime.today().strftime('%Y-%m-%d'))

        if duplicateAttendanceEntry.count() > 0:
            attendee.delete()
            continue

        isLate = 0

        # Heroku Scheduler has a fixed time this script runs at, which is 3:30 UTC.
        lateStartTime = timezone.now()
        lateEndTime = lateStartTime

        # Handle daylight savings offset.
        if not is_dst():
            lateStartTime -= datetime.timedelta(hours=2)
        else:
            lateStartTime -= datetime.timedelta(hours=3)
            lateEndTime -= datetime.timedelta(hours=1)

        # Update timezone info for the currently timezone-unaware datetime objects
        lateStartTime = lateStartTime.replace(tzinfo=pytz.UTC)
        lateEndTime = lateEndTime.replace(tzinfo=pytz.UTC)

        # Late deadline is 8:30 PM EST. The UTC time depends on whether Daylight Savings is in effect.
        # If member signs in late, mark him/her as late
        if (lateStartTime <= attendee.Time <= lateEndTime):
            isLate = 1

        # Proceed with saving attendance for this member
        attendance_entry = AttendanceHistory(First_Name = attendee.First_Name.title(), Last_Name = attendee.Last_Name.title(), Late = isLate)
        attendance_entry.save()

        # Get all matching records
        player = Players.objects.all().filter(First_Name__iexact = attendee.First_Name, Last_Name__iexact = attendee.Last_Name)

        # Player does not exist
        if len(player) == 0:
            new_player = Players(First_Name = attendee.First_Name, Last_Name = attendee.Last_Name, Standing = 6, Attendance = 1)
            new_player.save()

        # If player exists in database, update attendance record
        else:
            for p in player:

                p.Attendance += 1

                if isLate == 1:
                    p.Lateness += 1

                p.save()

        attendee.delete()
        hadPractice = True
        attendance_count += 1

    if hadPractice:
        duplicatePractice = Practices.objects.all().filter(Date = datetime.datetime.today().strftime('%Y-%m-%d'))

        if duplicatePractice.count() > 0:
            return;

        practice = Practices(Count = attendance_count)
        practice.save()




########## MAIN ##########

checkForUpdates()
checkAttendance()