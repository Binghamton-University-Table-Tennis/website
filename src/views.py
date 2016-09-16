from django.shortcuts import render
from django.http import HttpResponse

from .models import Greeting
from .models import Players
from .models import Matches
from LogTest import * 

def checkForUpdates():
    notYetUpdated = Matches.objects.all().filter(Updated = 0).order_by('Day')
    for m in notYetUpdated:
        winner = Players.objects.all().filter(First_Name = m.Winner_First_Name, Last_Name = m.Winner_Last_Name)
        loser = Players.objects.all().filter(First_Name = m.Loser_First_Name, Last_Name = m.Loser_Last_Name)
        win = winner[0].Rating
        lose = loser[0].Rating
        winPts = logRating(win, lose)

        m.Points = winPts[2]
        m.Winner_Rating = winPts[0]
        m.Loser_Rating = winPts[1]
        winnerMatchesPlayed = winner[0].Matches_Played + 1
        loserMatchesPlayed = loser[0].Matches_Played + 1
        winnerMatchesWon = winner[0].Matches_Won
        loserMatchesWon = loser[0].Matches_Won

        m.Updated = 1
        m.save()

        winner[0].Rating = winPts[0]
        loser[0].Rating = winPts[1]
        
        loser[0].Matches_Played += 1
        winner[0].Matches_Won += 1
        
        winner[0].Win_Rate = winnerMatchesWon / winnerMatchesPlayed
        loser[0].Win_Rate = loserMatchesWon / loserMatchesPlayed
        
        for w in winner:
            w.save(update_fields= ['Rating', 'Matches_Played']);
        for l in loser:
            l.save()
        

# Create your views here.
def index(request):
   
    # Store this visit to front page in the database
    visit = Greeting()
    visit.save()
    checkForUpdates()
    # Grab all players in database
    players = Players.objects.all().order_by('-Rating')
   
    return render(request, 'index.html', {'players': players})


def log(request):

    # Grab all visits to front page
    visits = Greeting.objects.all()
    
    return render(request, 'log.html', {'visits': visits})
    
def stats(request, player):
    name = player.split('_')
    player = Players.objects.all().filter(First_Name = name[0], Last_Name = name[1])
    
    matchesWon = Matches.objects.all().filter(Winner_First_Name = name[0], Winner_Last_Name = name[1])
    matchesLost = Matches.objects.all().filter(Loser_First_Name = name[0], Loser_Last_Name = name[1])
    
    matches = matchesWon | matchesLost
    matches.order_by('-Day')
    
    return render(request, 'stats.html', {'player': player[0], 'matches': matches})

