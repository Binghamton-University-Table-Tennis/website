from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from datetime import datetime, timedelta
from django.http import HttpResponseRedirect
from django.utils import timezone
import pytz

from .models import Greeting
from .models import Players
from .models import Matches
from .models import Practices
from .models import AttendanceHistory
from .models import Updates
from .models import Slides

from Ratings import *

# Create your views here.

def about(request):
    if request.user.is_authenticated():
        return render(request, 'about.html', {'admin': True})
    else:
        return render(request, 'about.html', {})

def photos(request):

    links = Slides.objects.all().order_by('Date')

    if request.user.is_authenticated():
        return render(request, 'photos.html', {'admin': True, 'links': links})
    else:
        return render(request, 'photos.html', {'links': links})

def rules(request):

    if request.user.is_authenticated():
        return render(request, 'rules.html', {'admin': True})
    else:
        return render(request, 'rules.html', {})

def ladder(request):

    # Determine who is still active in the club
    one_month_ago = timezone.now().date()
    one_month_ago -= timedelta(days=30)

    # Grab all players in database
    playersRanked = Players.objects.all().filter(Matches_Played__gt = 0).filter(LastSeen__gt = one_month_ago).order_by('-Rating')
    playersUnranked = Players.objects.all().filter(Matches_Played = 0, ).filter(LastSeen__gt = one_month_ago).order_by('-Rating')

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

    updates = Updates.objects.all().order_by('-Date');
    updateCount = len(updates)

    if request.user.is_authenticated():
        return render(request, 'index.html', {'error': False, 'admin': True, 'updates': updates, 'updateCount': updateCount})
    else:
        return render(request, 'index.html', {'error': False, 'updates': updates, 'updateCount': updateCount})


def log(request):

    # Only admins can view
    if not request.user.is_authenticated():
        return HttpResponseRedirect("/admin/")

    # Grab all visits to front page
    visits = Greeting.objects.all()

    # Grab other summary data
    players = Players.objects.all().order_by('-Attendance')
    practices = Practices.objects.all()

    # Get average number of members per practice
    sum = 0
    for practice in practices:
        sum += practice.Count

    average = sum / len(practices)

    # Get top 3 players with most attendance

    if len(players) >= 1:
        topAttendance = players[0].First_Name + " " + players[0].Last_Name

    return render(request, 'log.html', {'visits': visits, 'admin': True, 'numPlayers': len(players), 'numPractices': len(practices), 'average': average, 'topAttendance': topAttendance})

def attendance(request):

    # Only admins can view
    if not request.user.is_authenticated():
        return HttpResponseRedirect("/admin/")

    players = Players.objects.all().order_by('-Attendance')
    practices = Practices.objects.all().order_by('-Date')
    history = AttendanceHistory.objects.all()

    return render(request, 'attendance.html', {'players': players, 'practices': practices, 'history': history, 'admin': True})


def history(request, date):

    # Only admins can view
    if not request.user.is_authenticated():
        return HttpResponseRedirect("/admin/")

    # Format date so that it can be used in the filter. Some months are abbreviated with a period, some are not.
    if "." in date:
        date = str(date).replace("Sept", "Sep")     # Sept. must be converted to Sep. It's the only odd case
        parsed_date = datetime.strptime(date, '%b. %d, %Y').date()
    else:
        parsed_date = datetime.strptime(date, '%B %d, %Y').date()

    history = AttendanceHistory.objects.all().filter(Date = parsed_date, Late = 0).order_by('Last_Name')
    lateHistory = AttendanceHistory.objects.all().filter(Date = parsed_date, Late = 1).order_by('Last_Name')

    total = history.count() + lateHistory.count()

    return render(request, 'history.html', {'history': history, 'lateHistory': lateHistory, 'total': total, 'date': parsed_date, 'admin': True})

def stats(request, player):

    name = player.title().split()

    if len(name) != 2:
        if request.user.is_authenticated():
            return render(request, 'index.html', {'error': True, 'admin': True})
        else:
            return render(request, 'index.html', {'error': True})

    player = Players.objects.all().filter(First_Name = name[0], Last_Name = name[1])

    if len(player) != 1:
        if request.user.is_authenticated():
            return render(request, 'index.html', {'error': True, 'admin': True})
        else:
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

