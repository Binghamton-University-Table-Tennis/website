from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from datetime import datetime, timedelta
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

import sendgrid
import os
from sendgrid.helpers.mail import *

import pytz
import urllib
import urllib2
import json

from .models import Greeting
from .models import Players
from .models import Matches
from .models import Practices
from .models import AttendanceHistory
from .models import Updates
from .models import Slides
from .models import EBoard
from .models import Images
from .models import FrontPageContent
from .models import OrganizationInformation

from Ratings import *

# Create your views here.

def about(request):

    # Get jumbotron image for about us page
    photoList = Images.objects.all().filter(Page = Images.ABOUT)

    templateContext = {}

    if len(photoList) >= 1:
        templateContext['photo'] = photoList[0]

    if request.user.is_authenticated():
        templateContext['admin'] = True

    return render(request, 'about.html', templateContext)



def photos(request):

    links = Slides.objects.all().order_by('Date')

    templateContext = {'links': links}

    if request.user.is_authenticated():
        templateContext['admin'] = True

    return render(request, 'photos.html', templateContext)



def rules(request):

    photoList = Images.objects.all().filter(Page = Images.RULES)

    templateContext = {}

    if len(photoList) >= 1:
        templateContext['photo'] = photoList[0]

    if request.user.is_authenticated():
        templateContext['admin'] = True

    return render(request, 'rules.html', templateContext)



def ladder(request):

    # Determine who is still active in the club
    one_month_ago = timezone.now().date()
    one_month_ago -= timedelta(days=30)

    # Grab all players in database
    playersRanked = Players.objects.all().filter(Matches_Played__gt = 0).filter(LastSeen__gt = one_month_ago).order_by('-Rating')

    photoList = Images.objects.all().filter(Page = Images.LADDER)

    templateContext = {'playersRanked': playersRanked}

    if len(photoList) >= 1:
        templateContext['photo'] = photoList[0]

    if request.user.is_authenticated():
        templateContext['admin'] = True

    return render(request, 'ladder.html', templateContext)


@csrf_exempt
def contact(request):

    eboard = EBoard.objects.all()
    photoList = Images.objects.all().filter(Page = Images.CONTACT)

    # Determine if these API keys are set
    GOOGLE_RECAPTCHA_SITE_KEY = os.environ.get('GOOGLE_RECAPTCHA_SITE_KEY')
    GOOGLE_RECAPTCHA_SECRET_KEY = os.environ.get('GOOGLE_RECAPTCHA_SECRET_KEY')
    SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY')

    templateContext = {}

    if request.user.is_authenticated():
        templateContext['admin'] = True

    if GOOGLE_RECAPTCHA_SITE_KEY and GOOGLE_RECAPTCHA_SECRET_KEY and SENDGRID_API_KEY:
        templateContext['GOOGLE_RECAPTCHA_SITE_KEY'] = GOOGLE_RECAPTCHA_SITE_KEY

    if len(photoList) >= 1:
        templateContext['photo'] = photoList[0]

    templateContext['eboard'] = eboard

    return render(request, 'contact.html', templateContext)


def index(request):

    # Store this visit to front page in the database
    visits = Greeting.objects.all();

    for v in visits:
        v.Count += 1
        v.save()

    # Get all news/updates
    updates = Updates.objects.all().order_by('-Date');
    updateCount = len(updates)

    # Get all front page content
    frontPageContent = FrontPageContent.objects.all()

    # Get jumbotron image for home page
    photoList = Images.objects.all().filter(Page = Images.HOME)

    templateContext = {'error': False, 'updates': updates, 'updateCount': updateCount, 'frontPageContent': frontPageContent}

    if len(photoList) >= 1:
        templateContext['photo'] = photoList[0]

    if request.user.is_authenticated():
        templateContext['admin'] = True

    return render(request, 'index.html', templateContext)



def summary(request):

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

    if (len(practices) > 0):
        average = sum / len(practices)
    else:
        average = 0

    # Get player with most attendance
    if len(players) >= 1:
        topAttendance = players[0].First_Name + " " + players[0].Last_Name
    else:
        topAttendance = "N/A"

    # Determine number of players active in the club during the past 30 days
    one_month_ago = timezone.now().date()
    one_month_ago -= timedelta(days=30)
    numPlayersActive = len(Players.objects.all().filter(LastSeen__gt = one_month_ago))
    allPlayers = Players.objects.all()

    # Get active player with highest club rating
    players = Players.objects.all().filter(LastSeen__gt = one_month_ago).order_by('-Rating')
    if len(players) >= 1:
        topRating = players[0].First_Name + " " + players[0].Last_Name
    else:
        topRating = "N/A"

    # Get practice with the least players
    practices = Practices.objects.all().order_by('Count')
    if len(practices) >= 1:
        leastMembersDate = practices[0].Date
        leastMembersCount = practices[0].Count
    else:
        leastMembersDate = "N/A"
        leastMembersCount = 0

    # Get practice with the most players
    practices = Practices.objects.all().order_by('-Count')
    if len(practices) >= 1:
        mostMembersDate = practices[0].Date
        mostMembersCount = practices[0].Count
    else:
        mostMembersDate = "N/A"
        mostMembersCount = 0

    # Get class standing of all members
    freshmen = len(Players.objects.all().filter(Standing = 1))
    sophomores = len(Players.objects.all().filter(Standing = 2))
    juniors = len(Players.objects.all().filter(Standing = 3))
    seniors = len(Players.objects.all().filter(Standing = 4))
    grads = len(Players.objects.all().filter(Standing = 5))
    unknowns = len(Players.objects.all().filter(Standing = 6))

    # Get size of mailing list
    mailingListSize = len(Players.objects.all().exclude(Email = ''))

    # Get total number of ranked matches played
    numMatches = len(Matches.objects.all())

    # Get image URL for this page's banner
    photoList = Images.objects.all().filter(Page = Images.SUMMARY)

    templateContext = {'visits': visits, 'admin': True, 'numPlayers': len(allPlayers), 'numPractices': len(practices), 'average': average, 'topAttendance': topAttendance,
        'numPlayersActive': numPlayersActive, 'leastMembersDate': leastMembersDate, 'leastMembersCount': leastMembersCount, 'mostMembersDate': mostMembersDate, 'mostMembersCount': mostMembersCount,
        'freshmen': freshmen, 'sophomores': sophomores, 'juniors': juniors, 'seniors': seniors, 'grads': grads, 'unknowns': unknowns, 'mailingListSize': mailingListSize, 'topRating': topRating,
        'numMatches': numMatches
    }

    if len(photoList) >= 1:
        templateContext['photo'] = photoList[0]

    return render(request, 'summary.html', templateContext)


def attendance(request):

    # Only admins can view
    if not request.user.is_authenticated():
        return HttpResponseRedirect("/admin/")

    players = Players.objects.all().order_by('-Attendance')
    practices = Practices.objects.all().order_by('-Date')
    history = AttendanceHistory.objects.all()

    # Get image URL for this page's banner
    photoList = Images.objects.all().filter(Page = Images.ATTENDANCE)

    templateContext = {'players': players, 'practices': practices, 'history': history, 'admin': True}

    if len(photoList) >= 1:
        templateContext['photo'] = photoList[0]

    return render(request, 'attendance.html', templateContext)



def history(request, date):

    if date == "favicon.ico":
        return HttpResponse("Bad Date")

    dateObject = datetime.strptime(date, "%Y-%m-%d")

    # Only admins can view
    if not request.user.is_authenticated():
        return HttpResponseRedirect("/admin/")

    history = AttendanceHistory.objects.all().filter(Date = date).order_by('Time')

    return render(request, 'history.html', {'history': history, 'total': history.count(), 'date': dateObject, 'admin': True})

def stats(request, player):

    name = player.title().split()

    templateContext = {}

    if request.user.is_authenticated():
        templateContext['admin'] = True

    if len(name) != 2:
        templateContext['error'] = True
        return render(request, 'index.html', templateContext)

    player = Players.objects.all().filter(First_Name = name[0], Last_Name = name[1])

    if len(player) != 1:
        templateContext['error'] = True
        return render(request, 'index.html', {'error': True})

    matchesWon = Matches.objects.all().filter(Winner_First_Name__iexact = name[0], Winner_Last_Name__iexact = name[1])
    matchesLost = Matches.objects.all().filter(Loser_First_Name__iexact = name[0], Loser_Last_Name__iexact = name[1])

    matches = (matchesWon | matchesLost).order_by('-Day')
    standing = getStanding(player[0].Standing)

    templateContext = {'player': player[0], 'matches': matches, 'standing': standing}

    if request.user.is_authenticated():
        templateContext['admin'] = True

    return render(request, 'stats.html', templateContext)



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

@csrf_exempt
def sendemail(request):
    sender = request.POST.get('sender')
    subject = request.POST.get('subject')
    body = request.POST.get('body')

    if len(sender) == 0 or len(subject) == 0 or len(body) == 0:
        return HttpResponse("Empty Field")

    organizationList = OrganizationInformation.objects.all()
    organization = None

    if len(organizationList) >= 1:
        organization = organizationList[0]
    else:
        return HttpResponse("Organization Email Not Set")

    # Validate reCAPTCHA
    recaptcha_response = request.POST.get('g-recaptcha-response')
    url = 'https://www.google.com/recaptcha/api/siteverify'
    values = {
        'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
        'response': recaptcha_response
    }
    data = urllib.urlencode(values)
    req = urllib2.Request(url, data)
    response = urllib2.urlopen(req)
    result = json.load(response)

    if not result['success']:
        return HttpResponse("Bad reCAPTCHA Response")

    content = "FROM: " + sender + "\n"
    content += "\n----------------------------------------------------\n"
    content += "\n" + body + "\n"
    content += "\n----------------------------------------------------\n"
    content += "\nNote: This email was sent from " + request.get_host() + ". The authenticity of the sender cannot be verified."

    sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
    email_sender = Email(organization.Email)
    email_dest = Email(organization.Email)
    email_content = Content("text/plain", content)
    mail = Mail(email_sender, subject, email_dest, email_content)
    response = sg.client.mail.send.post(request_body=mail.get())

    if response.status_code >= 500:
        return HttpResponse("Service Unavailable")
    elif response.status_code >= 400:
        return HttpResponse("Bad Request")
    else:
        return HttpResponse("Success")