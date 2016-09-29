import django 
import os
import time
from datetime import date

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

django.setup()

from src.models import Greeting
from src.models import Players
from src.models import Matches
from src.Ratings import * 

def weeklyReward():
    #returns day of week, sunday is 6
    if(date.today().weekday() == 6):
        playersParticipated = Players.objects.all().filter(Played_This_Week = 1)
        for p in playersParticipated:
            p.Rating += 10;
            p.Played_This_Week = 0;
            p.save()
            
    
def checkForUpdates():

    #we extract all matches that haven't been put towards players' ratings, and sort them by the date the matches occurred
    notYetUpdated = Matches.objects.all().filter(Updated = 0).order_by('Day')
    #iterating over each match, we update the stats of the winner and loser for that match
    for m in notYetUpdated:
        winner = Players.objects.all().filter(First_Name = m.Winner_First_Name, Last_Name = m.Winner_Last_Name)
        loser = Players.objects.all().filter(First_Name = m.Loser_First_Name, Last_Name = m.Loser_Last_Name)
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
            w.Played_This_Week = 1
            l.Played_This_Week = 1
            
            w.save()
            l.save()
        
        if len(winPts) != 0:
            m.Points = winPts[2]
            m.Winner_Rating = winPts[0]
            m.Loser_Rating = winPts[1]
            m.Updated = 1
            m.save()


checkForUpdates()
weeklyReward()
