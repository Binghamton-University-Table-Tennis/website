from django.shortcuts import render
from django.http import HttpResponse

from .models import Greeting
from .models import Players

# Create your views here.
def index(request):
   
    # Store this visit to front page in the database
    greeting = Greeting()
    greeting.save()
    
    # Grab all players in database
    players = Players.objects.all()
    
    return render(request, 'index.html', {'players': players})


def db(request):

    # Grab all visits to front page
    greetings = Greeting.objects.all()

    return render(request, 'db.html', {'greetings': greetings})

