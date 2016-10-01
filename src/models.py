from django.db import models

# Create your models here.
class Greeting(models.Model):
    Count = models.IntegerField(editable=False, default = 0)
    
    class Meta:
        db_table = "visits"
        verbose_name_plural = "Visits"

    def __unicode__(self):
       return self.Time

class Players(models.Model):
    First_Name = models.CharField(max_length=20)
    Last_Name = models.CharField(max_length=20)
    Rating = models.IntegerField(editable=False, default=1000)
    Matches_Won = models.IntegerField(editable=False, default=0)
    Matches_Lost = models.IntegerField(editable=False, default=0)
    Matches_Played = models.IntegerField(editable=False, default=0)
    Win_Rate =models.IntegerField(editable=False, default=0)
    Standing = models.IntegerField(choices=[(x, x) for x in range(1, 6)])
    Played_This_Week = models.IntegerField(editable=False, default=0)
    Attendance = models.IntegerField(editable=False, default=0)
    
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
    Winner_Score = models.IntegerField()
    Loser_Score = models.IntegerField()
    Day = models.DateTimeField('date created', auto_now_add=True, editable=False)
    Points = models.IntegerField(editable=False, default=0)
    Winner_Rating = models.IntegerField(editable=False, default=0)
    Loser_Rating = models.IntegerField(editable=False, default=0)
    Updated = models.IntegerField(editable=False, default=0)
    
    class Meta:
        db_table = "matches"
        verbose_name_plural = "Matches"

    def __unicode__(self):
       return (self.Winner_Last_Name + " vs " + self.Loser_Last_Name)

class ClubAttendance(models.Model):
    First_Name = models.CharField(max_length=20)
    Last_Name = models.CharField(max_length=20)

    class Meta:
        db_table = "attendance"
        verbose_name_plural = "Club Attendance"

    def __unicode__(self):
       return (self.First_Name + " " + self.Last_Name)
    