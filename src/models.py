from django.db import models

# Create your models here.
class Greeting(models.Model):
    time = models.DateTimeField('date created', auto_now_add=True)
    
    class Meta:
        db_table = "visits"

class Players(models.Model):
    lastname = models.CharField(max_length=10)
    firstname = models.CharField(max_length=10)
    rating = models.IntegerField()
    
    class Meta:
        db_table = "players"

class Matches(models.Model):
    winner_fname = models.CharField(max_length=10)
    winner_lname = models.CharField(max_length=10)
    loser_fname = models.CharField(max_length=10)
    loser_lname = models.CharField(max_length=10)
    winner_score = models.IntegerField()
    loser_score = models.IntegerField()
    day = models.DateField()
    
    class Meta:
        db_table = "matches"
    