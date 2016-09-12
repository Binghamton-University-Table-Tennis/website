from django.db import models

# Create your models here.
class Greeting(models.Model):
    time = models.DateTimeField('date created', auto_now_add=True)

class Players(models.Model):
    lastname = models.CharField(max_length=10)
    firstname = models.CharField(max_length=10)
    rating = models.IntegerField()
    
    class Meta:
        db_table = "players"
    