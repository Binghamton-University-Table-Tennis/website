from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from datetime import datetime

from .models import Greeting
from .models import Players
from .models import Matches
from .models import Practices
from .models import AttendanceHistory

from Ratings import * 

# Create your views here.

def about(request):
    if request.user.is_authenticated():   
        return render(request, 'about.html', {'admin': True})
    else:
        return render(request, 'about.html', {})    
        
def rules(request):
    
    if request.user.is_authenticated():   
        return render(request, 'rules.html', {'admin': True})
    else:
        return render(request, 'rules.html', {})

def ladder(request):
    
    # Grab all players in database
    playersRanked = Players.objects.all().filter(Matches_Played__gt = 0).order_by('-Rating')
    playersUnranked = Players.objects.all().filter(Matches_Played = 0).order_by('-Rating')

    if request.user.is_authenticated():   
        return render(request, 'ladder.html', {'playersRanked': playersRanked, 'playersUnranked': playersUnranked, 'admin': True})
    else:
        return render(request, 'ladder.html', {'playersRanked': playersRanked, 'playersUnranked': playersUnranked})
    
def contact(request):
    
    if request.user.is_authenticated():   
        return render(request, 'contact.html', {'admin': True})
    else:
        return render(request, 'contact.html', {})
    
def index(request):
    
        
    # Store this visit to front page in the database
    visits = Greeting.objects.all();
        
    for v in visits:
        v.Count += 1
        v.save()
        
    if request.user.is_authenticated():   
        return render(request, 'index.html', {'error': False, 'admin': True})
    else:                                       
        return render(request, 'index.html', {'error': False})


def log(request):

    # Only admins can view
    if not request.user.is_authenticated():
        return render(request, 'index.html', {'error': False})
        
    # Grab all visits to front page
    visits = Greeting.objects.all()
    
    if request.user.is_authenticated():   
        return render(request, 'log.html', {'visits': visits, 'admin': True})
    else:       
        return render(request, 'log.html', {'visits': visits})
    
def attendance(request):
    
    # Only admins can view
    if not request.user.is_authenticated():
        return render(request, 'index.html', {'error': False})
    
    players = Players.objects.all().order_by('-Attendance')
    practices = Practices.objects.all().order_by('-Date')
    history = AttendanceHistory.objects.all()
    
    if request.user.is_authenticated():   
        return render(request, 'attendance.html', {'players': players, 'practices': practices, 'history': history, 'admin': True})
    else:       
        return render(request, 'attendance.html', {'players': players, 'practices': practices, 'history': history})

    
def history(request, date):
    
    # Only admins can view
    if not request.user.is_authenticated():
        return render(request, 'index.html', {'error': False})
        
    # Format date so that it can be used in the filter. Some months are abbreviated with a period, some are not.
    if "." in date:
        date = str(date).replace("Sept", "Sep")     # Sept. must be converted to Sep. It's the only odd case
        parsed_date = datetime.strptime(date, '%b. %d, %Y').date()
    else:
        parsed_date = datetime.strptime(date, '%B %d, %Y').date()

    history = AttendanceHistory.objects.all().filter(Date = parsed_date).order_by('Last_Name')
    
    if request.user.is_authenticated():   
        return render(request, 'history.html', {'history': history, 'date': str(parsed_date), 'admin': True})
    else:       
        return render(request, 'history.html', {'history': history, 'date': str(parsed_date)})
        

def stats(request, player):

    name = player.title().split()
    
    if len(name) != 2:
        return render(request, 'index.html', {'error': True})
    
    player = Players.objects.all().filter(First_Name = name[0], Last_Name = name[1])

    if len(player) != 1:
        return render(request, 'index.html', {'error': True})
    
    matchesWon = Matches.objects.all().filter(Winner_First_Name__iexact = name[0], Winner_Last_Name__iexact = name[1])
    matchesLost = Matches.objects.all().filter(Loser_First_Name__iexact = name[0], Loser_Last_Name__iexact = name[1])
    
    matches = (matchesWon | matchesLost).order_by('-Day')

    standing = getStanding(player[0].Standing)
    
    if request.user.is_authenticated():   
        return render(request, 'stats.html', {'player': player[0], 'matches': matches, 'standing': standing, 'admin': True})
    else:
        return render(request, 'stats.html', {'player': player[0], 'matches': matches, 'standing': standing})
    
def getStanding(standing):
    classStanding = ""
    
    if standing == 1:
        classStanding = "Freshman"
    elif standing == 2:
        classStanding = "Sophomore"   
    elif standing == 3:
        classStanding = "Junior"  
    elif standing == 4:
        classStanding = "Senior"  
    elif standing == 5:
        classStanding = "Grad"
    else:
        classStanding = "Unknown"
    
    return classStanding
    
def search(request):
    result = request.GET.get('searchName')
    return redirect('stats', player=result)
    
