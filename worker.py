import django
import os
import time
from datetime import date
import datetime
from django.utils import timezone
import pytz

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

django.setup()

from src.models import Greeting
from src.models import Players
from src.models import Matches
from src.models import Practices
from src.models import AttendanceHistory

from src.Ratings import *
from src.Standings import *

def checkForMatchUpdates():

    # Extract all matches that haven't been put towards players' ratings, and sort them by the date the matches occurred
    notYetUpdated = Matches.objects.all().filter(Updated = 0).order_by('Day')

    # Iterate over each match and update the stats of the winner and loser for that match
    for match in notYetUpdated:
        winner = Players.objects.all().filter(First_Name__iexact = match.Winner_First_Name, Last_Name__iexact = match.Winner_Last_Name)
        loser = Players.objects.all().filter(First_Name__iexact = match.Loser_First_Name, Last_Name__iexact = match.Loser_Last_Name)
        win = 0
        lose = 0
        winPts = []

        for w, l in zip(winner, loser):

            # Delete entry if winner and loser are the same person
            if w.First_Name.title() == l.First_Name.title() and w.Last_Name.title() == l.Last_Name.title():
                match.delete()
                break

            win = w.Rating
            lose = l.Rating

            # Call function that calculates how much the players' ratings should change, based on their difference in skill level
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

            w.save()
            l.save()

        if len(winPts) != 0:
            match.Points = winPts[2]
            match.Winner_Rating = winPts[0]
            match.Loser_Rating = winPts[1]
            match.Updated = 1
            match.save()



def checkForPracticeUpdates():
    attendances = AttendanceHistory.objects.all().filter(Updated = 0)
    practices = Practices.objects.all()
    oldPractices = {}
    newPractices = {}

    # Get all known practices
    for practice in practices:
        if practice.Date not in oldPractices:
            oldPractices[practice.Date] = 1


    # Check for attendees with dates that are not in the practice table
    for attendance in attendances:

        # Check for duplicates
        duplicateAttendanceEntry = AttendanceHistory.objects.all().filter(First_Name__iexact = attendance.First_Name, Last_Name__iexact = attendance.Last_Name, Date = attendance.Date)

        if duplicateAttendanceEntry.count() > 1:
            attendance.delete()
            continue


        # Get all matching player records
        player = Players.objects.all().filter(First_Name__iexact = attendance.First_Name, Last_Name__iexact = attendance.Last_Name)

        if len(player) == 0:
            # Player does not exist. Create new entry.
            new_player = Players(First_Name = attendance.First_Name.title(), Last_Name = attendance.Last_Name.title(), Standing = 6, Attendance = 1, LastSeen = timezone.now().date())
            new_player.save()
        else:
            # Player exists. Update attendance.
            for p in player:
                p.LastSeen = timezone.now().date()
                p.Attendance += 1
                p.save()


        # Determine if this is a new practice or not
        if attendance.Date in oldPractices:
            oldPractice = Practices.objects.all().filter(Date = attendance.Date)[0]
            oldPractice.Count += 1
            oldPractice.save()
        else:
            if attendance.Date not in newPractices:
                newPractices[attendance.Date] = 0

            newPractices[attendance.Date] += 1

        # Check if member wants to join the mailing list
        if attendance.Email != '' and '@' in attendance.Email:
            player = Players.objects.all().filter(First_Name__iexact = attendance.First_Name, Last_Name__iexact = attendance.Last_Name)
            for p in player:
                p.Email = attendance.Email
                p.save()

        # Check if member specified class standing
        if attendance.Class_Standing != '':
            player = Players.objects.all().filter(First_Name__iexact = attendance.First_Name, Last_Name__iexact = attendance.Last_Name)
            for p in player:
                p.Standing = getIntegerStanding(attendance.Class_Standing)
                p.save()

        # Mark as updated
        attendance.Updated = 1
        attendance.save()

    # Save all new practices
    for practiceDate, count in newPractices.items():
        newPractice = Practices(Date = practiceDate, Count = count)
        newPractice.save()




def createPageVisitsTable():
    # Make sure the page count tracker exists
    visits = Greeting.objects.all()
    if len(visits) == 0:
        visitObject = Greeting(Count = 0)
        visitObject.save()




########## MAIN ##########

checkForMatchUpdates()
checkForPracticeUpdates()
createPageVisitsTable()
