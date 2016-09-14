from django.shortcuts import render
from django.http import HttpResponse

from .models import Greeting
from .models import Players
from .models import Matches

# Create your views here.
def index(request):
   
    # Store this visit to front page in the database
    visit = Greeting()
    visit.save()
    
    # Grab all players in database
    players = Players.objects.all().order_by('-rating')
    
    return render(request, 'index.html', {'players': players})


def log(request):

    # Grab all visits to front page
    visits = Greeting.objects.all()
    
    return render(request, 'log.html', {'visits': visits})
    
def stats(request, player):
    name = player.split('_')
    playerStats = Players.objects.all().filter(firstname = name[0], lastname = name[1])
    matchesWon = Matches.objects.all().filter(winner_fname = name[0], winner_lname = name[1])
    matchesLost = Matches.objects.all().filter(loser_fname = name[0], loser_lname = name[1])
    matches = matchesWon | matchesLost
    matches.order_by('-day')
    return render(request, 'stats.html', {'playerStats': playerStats[0], 'matches': matches, 'fname': name[0], 'lname': name[1]})

