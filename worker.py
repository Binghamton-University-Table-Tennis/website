import django 
import os
import time
from datetime import date
import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

django.setup()

from src.models import Greeting
from src.models import Players
from src.models import Matches
from src.models import ClubAttendance
from src.models import Practices
from src.models import AttendanceHistory

from src.Ratings import * 

def weeklyReward():
    #returns day of week, friday is 4
    if(date.today().weekday() == 4):
        playersParticipated = Players.objects.all().filter(Played_This_Week = 1)
        for p in playersParticipated:

            match = Matches(Winner_First_Name = p.First_Name, Winner_Last_Name = p.Last_Name, Loser_First_Name = "Weekly", Loser_Last_Name ="Participation", Winner_Score=0, Loser_Score=0, Points=10, Winner_Rating=p.Rating+10, Updated=1)
            match.save()
            
            p.Rating += 10;
            p.Played_This_Week = 0;
            p.save()
            

            
    
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
    
    for attendee in attendees:
        
        # Check for duplicate attendance entries
        duplicateAttendee = ClubAttendance.objects.all().filter(First_Name__iexact = attendee.First_Name, Last_Name__iexact = attendee.Last_Name)
        
        if duplicateAttendee.count() > 1:
            attendee.delete()
            continue
        
        # Proceed with saving attendance for this member
        player = Players.objects.all().filter(First_Name__iexact = attendee.First_Name, Last_Name__iexact = attendee.Last_Name)
        
        for p in player:
            
            # Check for existing entry for this player in attendance history for today
            duplicateAttendanceEntry = AttendanceHistory.objects.all().filter(First_Name__iexact = p.First_Name, Last_Name__iexact = p.Last_Name, Date = datetime.datetime.today().strftime('%Y-%m-%d'))
            
            if duplicateAttendanceEntry.count() > 0:
                break;
            
            p.Attendance += 1
            p.save()
            attendance_entry = AttendanceHistory(First_Name = p.First_Name.title(), Last_Name = p.Last_Name.title())
            attendance_entry.save()

        attendee.delete()
        hadPractice = True

    if hadPractice:
        duplicatePractice = Practices.objects.all().filter(Date = datetime.datetime.today().strftime('%Y-%m-%d'))
        
        if duplicatePractice.count() > 0:
            return;
            
        practice = Practices()
        practice.save()


########## MAIN ##########

checkForUpdates()
checkAttendance()