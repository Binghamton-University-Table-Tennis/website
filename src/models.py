from django.db import models

# Create your models here.
class Greeting(models.Model):
    Time = models.DateTimeField('date created', auto_now_add=True)
    
    class Meta:
        db_table = "visits"
        verbose_name_plural = "Visits"

    def __unicode__(self):
       return self.Time

class Players(models.Model):
    First_Name = models.CharField(max_length=10)
    Last_Name = models.CharField(max_length=10)
    Rating = models.IntegerField()
    Matches_Won = models.IntegerField(editable=False, default=0)
    Matches_Played = models.IntegerField(editable=False, default=0)
    Win_Rate =models.IntegerField(editable=False, default=0)
    Standing = models.IntegerField()
    
    class Meta:
        db_table = "players"
        verbose_name_plural = "Players"

    def __unicode__(self):
       return (self.First_Name + " " + self.Last_Name)

class Matches(models.Model):
    Winner_First_Name = models.CharField(max_length=10)
    Winner_Last_Name = models.CharField(max_length=10)
    Loser_First_Name = models.CharField(max_length=10)
    Loser_Last_Name = models.CharField(max_length=10)
    Winner_Score = models.IntegerField()
    Loser_Score = models.IntegerField()
    Day = models.DateField()
    Points = models.IntegerField(editable=False, default=0)
    Winner_Rating = models.IntegerField(editable=False, default=0)
    Loser_Rating = models.IntegerField(editable=False, default=0)
    Updated = models.IntegerField(editable=False, default=0)
    
    class Meta:
        db_table = "matches"
        verbose_name_plural = "Matches"

    def __unicode__(self):
       return (self.Winner_Last_Name + " vs " + self.Loser_Last_Name)
    