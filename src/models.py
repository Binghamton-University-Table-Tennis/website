from django.db import models
from django.utils import timezone

# Create your models here.
class Greeting(models.Model):
    Count = models.IntegerField(editable=False, default = 0)

    def get_absolute_url(self):
        return "/summary"

    class Meta:
        db_table = "visits"
        verbose_name_plural = "Visits"

    def __unicode__(self):
       return "Front page visits: " + str(self.Count)

class Players(models.Model):
    First_Name = models.CharField(max_length=20)
    Last_Name = models.CharField(max_length=20)
    Rating = models.IntegerField(editable=False, default=1000)
    Matches_Won = models.IntegerField(editable=False, default=0)
    Matches_Lost = models.IntegerField(editable=False, default=0)
    Matches_Played = models.IntegerField(editable=False, default=0)
    Win_Rate =models.IntegerField(editable=False, default=0)
    Standing = models.IntegerField(choices=[(1, "Freshman"), (2, "Sophomore"), (3, "Junior"), (4, "Senior"), (5, "Grad"), (6, "Unknown")])
    Played_This_Week = models.IntegerField(editable=False, default=0)
    Attendance = models.IntegerField(editable=False, default=0)
    Lateness = models.IntegerField(editable=False, default=0)
    LastSeen = models.DateField(editable=False, default=timezone.now)

    def get_absolute_url(self):
        return "/attendance"

    class Meta:
        db_table = "players"
        verbose_name_plural = "Players"

    def __unicode__(self):
       return (self.First_Name + " " + self.Last_Name)

class Matches(models.Model):
    Winner_First_Name = models.CharField(max_length=20)
    Winner_Last_Name = models.CharField(max_length=20)
    Loser_First_Name = models.CharField(max_length=20)
    Loser_Last_Name = models.CharField(max_length=20)
    Winner_Score = models.IntegerField(choices=[(2,2)])
    Loser_Score = models.IntegerField(choices=[(x,x) for x in range(2)])
    Day = models.DateTimeField('date created', auto_now_add=True, editable=False)
    Points = models.IntegerField(editable=False, default=0)
    Winner_Rating = models.IntegerField(editable=False, default=0)
    Loser_Rating = models.IntegerField(editable=False, default=0)
    Updated = models.IntegerField(editable=False, default=0)

    def get_absolute_url(self):
        return "/ladder"

    class Meta:
        db_table = "matches"
        verbose_name_plural = "Matches"

    def __unicode__(self):
       return (self.Winner_Last_Name + " vs " + self.Loser_Last_Name)

class ClubAttendance(models.Model):
    First_Name = models.CharField(max_length=20)
    Last_Name = models.CharField(max_length=20)
    Time = models.DateTimeField('date created', auto_now_add=True, editable=False)

    class Meta:
        db_table = "attendance"
        verbose_name_plural = "Club Attendance"

    def __unicode__(self):
       return (self.First_Name + " " + self.Last_Name)

class Practices(models.Model):
    Date = models.DateField(auto_now_add=True, editable=False)
    Count = models.IntegerField(editable=False, default=0)

    def get_absolute_url(self):
        return "/attendance"

    class Meta:
        db_table = "practices"
        verbose_name_plural = "Practices"

    def __unicode__(self):
       return str(self.Date)

class AttendanceHistory(models.Model):
    First_Name = models.CharField(max_length=20)
    Last_Name = models.CharField(max_length=20)
    Date = models.DateField(auto_now_add=True, editable=False)
    Late = models.IntegerField(editable=False, default=0)

    def get_absolute_url(self):
        return "/attendance"

    class Meta:
        db_table = "attendance_history"
        verbose_name_plural = "Past Attendance"

    def __unicode__(self):
       return str(self.Date) + ": " + self.First_Name + " " + self.Last_Name

class Updates(models.Model):
    Date = models.DateField()
    Message = models.CharField(max_length=200)

    def get_absolute_url(self):
        return "/"

    class Meta:
        db_table = "updates"
        verbose_name_plural = "Updates"

    def __unicode__(self):
       return str(self.Date) + ": " + self.Message

class Slides(models.Model):
    Date = models.DateField()
    Title = models.CharField(max_length=100)

    ########## How to get the SlidesID ##########
    # Full URL = https://docs.google.com/presentation/d/1152Jzvxr-hDXlGE1zaT4_NuZf8sl-GAIvCUhhzMA800/edit#slide=id.g1b0ebe7be8_0_0
    # SlidesID = 1152Jzvxr-hDXlGE1zaT4_NuZf8sl-GAIvCUhhzMA800
    SlidesID = models.CharField(max_length=100)

    def get_absolute_url(self):
        return "/photos"

    class Meta:
        db_table = "slides"
        verbose_name_plural = "Slides"

    def __unicode__(self):
       return str(self.Title)

class EBoard(models.Model):
    Name = models.CharField(max_length=50)
    Position = models.IntegerField(choices=[(1, "President"), (2, "Co-President"), (3, "Treasurer"), (4, "Secretary"), (5, "Webmaster")])

    def get_absolute_url(self):
        return "/contact"

    class Meta:
        db_table = "eboard"
        verbose_name_plural = "EBoard"

    def __unicode__(self):
       return str(self.Name)

class Images(models.Model):
    BACKGROUND = 1
    INDEX = 2
    ATTENDANCE = 3
    SUMMARY = 4
    LADDER = 5
    ABOUT = 6
    RULES = 7
    CONTACT = 8

    PAGE_CHOICES = (
        (BACKGROUND, "background"),
        (INDEX, "index"),
        (ATTENDANCE, "attendance"),
        (SUMMARY, "summary"),
        (LADDER, "ladder"),
        (ABOUT, "about"),
        (RULES, "rules"),
        (CONTACT, "contact")
    )

    Page = models.IntegerField(choices=PAGE_CHOICES)
    URL = models.CharField(max_length=200)

    def get_absolute_url(self):
        return "/"

    class Meta:
        db_table = "images"
        verbose_name_plural = "Images"

    def __unicode__(self):
       return str(self.get_Page_display())


class OrganizationInformation(models.Model):
    Name = models.CharField(max_length=100)
    Email = models.CharField(max_length=100)
    Address1 = models.CharField(max_length=100)
    Address2 = models.CharField(max_length=100)
    Copyright_Year = models.CharField(max_length=20)
    Description = models.CharField(max_length=500)

    def get_absolute_url(self):
        return "/"

    class Meta:
        db_table = "organization_information"
        verbose_name_plural = "Organization Information"

    def __unicode__(self):
       return str(self.Name)

class FrontPageContent(models.Model):
    Title = models.CharField(max_length=100)
    Description = models.CharField(max_length=500)

    def get_absolute_url(self):
        return "/"

    class Meta:
        db_table = "front_page_content"
        verbose_name_plural = "Front Page Content"

    def __unicode__(self):
       return str(self.Title)


class SocialMedia(models.Model):
    Website_URL = models.CharField(max_length=100)
    Logo_URL = models.CharField(max_length=100)

    def get_absolute_url(self):
        return "/"

    class Meta:
        db_table = "social_media"
        verbose_name_plural = "Social Media"

    def __unicode__(self):
       return str(self.Website_URL)


class ColorScheme(models.Model):

    RED = '#ff0000'
    ORANGE = 'ffa500'
    YELLOW = 'ffff00'
    GREEN = '#005a43'
    BLUE = '#0000ff'
    INDIGO = '#4b0082'
    VIOLET = '#8a2be2'
    GRAY = '#808080'
    BLACK = '#000000'

    COLOR_CHOICES = (
        (RED, "Red"),
        (ORANGE, "Orange"),
        (YELLOW, "Yellow"),
        (GREEN, "Green"),
        (BLUE, "Blue"),
        (INDIGO, "Indigo"),
        (VIOLET, "Violet"),
        (GRAY, "Gray"),
        (BLACK, "Black")
    )

    Color = models.CharField(choices=COLOR_CHOICES, max_length=10)

    def get_absolute_url(self):
        return "/"

    class Meta:
        db_table = "color_scheme"
        verbose_name_plural = "Color Scheme"

    def __unicode__(self):
       return str(self.get_Color_display())