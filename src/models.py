from django.db import models

# Create your models here.
class Greeting(models.Model):
    time = models.DateTimeField('date created', auto_now_add=True)
    
    class Meta:
        db_table = "visits"
        verbose_name_plural = "Visits"
        
    def __unicode__(self):
       return self.time

class Players(models.Model):
    id = models.IntegerField(primary_key=True)
    last_name = models.CharField(max_length=10)
    first_name = models.CharField(max_length=10)
    rating = models.IntegerField()
    matches_won = models.IntegerField(editable=False, default=0)
    matches_played = models.IntegerField(editable=False, default=0)
    win_rate =models.IntegerField(editable=False, default=0)
    standing = models.IntegerField()
    
    class Meta:
        db_table = "players"
        verbose_name_plural = "Players"
        
    def __unicode__(self):
       return (self.first_name + " " + self.last_name)

class Matches(models.Model):
    id = models.IntegerField(primary_key=True)
    winner_first_name = models.CharField(max_length=10)
    winner_last_name = models.CharField(max_length=10)
    loser_first_name = models.CharField(max_length=10)
    loser_last_name = models.CharField(max_length=10)
    winner_score = models.IntegerField()
    loser_score = models.IntegerField()
    day = models.DateField()
    points = models.IntegerField(editable=False)
    winner_rating = models.IntegerField(editable=False)
    loser_rating = models.IntegerField(editable=False)
    
    class Meta:
        db_table = "matches"
        verbose_name_plural = "Matches"
        
    def __unicode__(self):
       return (self.winner_last_name + " vs " + self.loser_last_name)
    