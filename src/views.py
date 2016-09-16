from django.shortcuts import render
from django.http import HttpResponse

from .models import Greeting
from .models import Players
from .models import Matches
from LogTest import * 

#updates player's stats only if they haven't been updated, occurs before the page is rendered
def checkForUpdates():
    notYetUpdated = Matches.objects.all().filter(Updated = 0).order_by('Day')
    for m in notYetUpdated:
        winner = Players.objects.all().filter(First_Name = m.Winner_First_Name, Last_Name = m.Winner_Last_Name)
        loser = Players.objects.all().filter(First_Name = m.Loser_First_Name, Last_Name = m.Loser_Last_Name)
        win = 0
        lose = 0
        winPts = []

        for w, l in zip(winner, loser):
            win = w.Rating
            lose = l.Rating
            winPts = logRating(win, lose)

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
            
            # Calculate win rate - need to use floats to force floating point arithmetic
            w.Win_Rate = int((float(winnerMatchesWon) / winnerMatchesPlayed)*100)
            l.Win_Rate = int((float(loserMatchesWon) / loserMatchesPlayed)*100)
            
            w.save()
            l.save()
        
        m.Points = winPts[2]
        m.Winner_Rating = winPts[0]
        m.Loser_Rating = winPts[1]
        m.Updated = 1
        m.save()

# Create your views here.
def index(request):
   
    # Store this visit to front page in the database
    visit = Greeting()
    visit.save()
    
    # Check if there are matches to be processed
    checkForUpdates()
    
    # Grab all players in database
    players = Players.objects.all().order_by('-Rating')
   
    return render(request, 'index.html', {'players': players})


def log(request):

    # Grab all visits to front page
    visits = Greeting.objects.all()
    
    return render(request, 'log.html', {'visits': visits})
    
def stats(request, player):
    
    # Check if there are matches to be processed
    checkForUpdates()
    
    name = player.split('_')
    player = Players.objects.all().filter(First_Name = name[0], Last_Name = name[1])
    
    matchesWon = Matches.objects.all().filter(Winner_First_Name = name[0], Winner_Last_Name = name[1])
    matchesLost = Matches.objects.all().filter(Loser_First_Name = name[0], Loser_Last_Name = name[1])
    
    matches = matchesWon | matchesLost
    matches.order_by('-Day')
    
    medal = getMedal(player[0].Rating)
    
    return render(request, 'stats.html', {'player': player[0], 'matches': matches, 'medal': medal})

def getMedal(rating):
    medal = ""
    if rating <= 1050:
        medal = "Bronze"
    elif rating <= 1100:
        medal = "Silver"
    elif rating <= 1150:
        medal = "Gold"
    elif rating <= 1200:
        medal = "Platinum"
    elif rating <= 1250:
        medal = "Diamond"
    elif rating <= 1300:
        medal = "Crystal"
    else:
        medal = "Ruby"
        
    return medal