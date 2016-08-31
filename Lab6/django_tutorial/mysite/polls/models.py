import datetime

from django.db import models
from django.utils import timezone
from geopy.geocoders import Nominatim

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    loc = models.CharField(max_length=200, blank= True)
    lati = models.FloatField(default=0)
    long = models.FloatField(default=0)
    weather = models.CharField(max_length=500, blank= True)
  
    def __str__(self):
        return self.question_text
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    loc = models.CharField(max_length=200, blank= True)
    lati = models.FloatField(default=0)
    long = models.FloatField(default=0)
    weather = models.CharField(max_length=500, blank= True)
    votes = models.IntegerField(default=0)
    def __str__(self):
        return self.choice_text
        
            