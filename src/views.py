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

