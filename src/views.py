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

    if len(photoList) == 1:
        photo = photoList[0]

        if request.user.is_authenticated():
            return render(request, 'about.html', {'admin': True, 'photo': photo})
        else:
            return render(request, 'about.html', {'photo': photo})
    else:
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

    photoList = Images.objects.all().filter(Page = Images.RULES)

    if len(photoList) == 1:
        photo = photoList[0]

        if request.user.is_authenticated():
            return render(request, 'rules.html', {'admin': True, 'photo': photo})
        else:
            return render(request, 'rules.html', {'photo': photo})
    else:
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

    photoList = Images.objects.all().filter(Page = Images.LADDER)

    if len(photoList) == 1:
        photo = photoList[0]

        if request.user.is_authenticated():
            return render(request, 'ladder.html', {'playersRanked': playersRanked, 'playersUnranked': playersUnranked, 'admin': True, 'photo': photo})
        else:
            return render(request, 'ladder.html', {'playersRanked': playersRanked, 'playersUnranked': playersUnranked, 'photo': photo})
    else:
        if request.user.is_authenticated():
            return render(request, 'ladder.html', {'playersRanked': playersRanked, 'playersUnranked': playersUnranked, 'admin': True})
        else:
            return render(request, 'ladder.html', {'playersRanked': playersRanked, 'playersUnranked': playersUnranked})

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
    photoList = Images.objects.all().filter(Page = Images.INDEX)

    if len(photoList) == 1:
        photo = photoList[0]

        if request.user.is_authenticated():
            return render(request, 'index.html', {'error': False, 'admin': True, 'updates': updates, 'updateCount': updateCount, 'photo': photo, 'frontPageContent': frontPageContent})
        else:
            return render(request, 'index.html', {'error': False, 'updates': updates, 'updateCount': updateCount, 'photo': photo, 'frontPageContent': frontPageContent})
    else:
        if request.user.is_authenticated():
            return render(request, 'index.html', {'error': False, 'admin': True, 'updates': updates, 'updateCount': updateCount, 'frontPageContent': frontPageContent})
        else:
            return render(request, 'index.html', {'error': False, 'updates': updates, 'updateCount': updateCount, 'frontPageContent': frontPageContent})


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

    # Get image URL for this page's banner
    photoList = Images.objects.all().filter(Page = Images.SUMMARY)

    if len(photoList) == 1:
        photo = photoList[0]

        return render(request, 'summary.html', {'visits': visits, 'admin': True, 'numPlayers': len(players), 'numPractices': len(practices), 'average': average, 'topAttendance': topAttendance, 'photo': photo})
    else:
        return render(request, 'summary.html', {'visits': visits, 'admin': True, 'numPlayers': len(players), 'numPractices': len(practices), 'average': average, 'topAttendance': topAttendance})


def attendance(request):

    # Only admins can view
    if not request.user.is_authenticated():
        return HttpResponseRedirect("/admin/")

    players = Players.objects.all().order_by('-Attendance')
    practices = Practices.objects.all().order_by('-Date')
    history = AttendanceHistory.objects.all()

    # Get image URL for this page's banner
    photoList = Images.objects.all().filter(Page = Images.ATTENDANCE)

    if len(photoList) == 1:
        photo = photoList[0]

        return render(request, 'attendance.html', {'players': players, 'practices': practices, 'history': history, 'admin': True, 'photo': photo})
    else:
        return render(request, 'attendance.html', {'players': players, 'practices': practices, 'history': history, 'admin': True})


def history(request, date):

    if date == "favicon.ico":
        return HttpResponse("Bad Date")

    dateObject = datetime.strptime(date, "%Y-%m-%d")

    # Only admins can view
    if not request.user.is_authenticated():
        return HttpResponseRedirect("/admin/")

    history = AttendanceHistory.objects.all().filter(Date = date).order_by('Last_Name')

    return render(request, 'history.html', {'history': history, 'total': history.count(), 'date': dateObject, 'admin': True})

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