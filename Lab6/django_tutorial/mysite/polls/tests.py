from polls.models import Question, Choice
from geopy.geocoders import Nominatim
Question.objects.all()
from django.utils import timezone

geolocator = Nominatim()
location_1 = geolocator.geocode("London,UK")
location_2 = geolocator.geocode("New York City,USA")
location_3 = geolocator.geocode("Boston,USA")
location_4 = geolocator.geocode("San Francisco,USA")

import pyowm
API_key = 'ba6d8b69ab594472e4f0d73c1a92ffd2'

owm = pyowm.OWM(API_key)

obs_1 = owm.weather_at_place('London,uk')
w_1 = obs_1.get_weather()

obs_2 = owm.weather_at_place("NewYork,USA")
w_2 = obs_2.get_weather()

obs_3 = owm.weather_at_place("Boston,USA")
w_3 = obs_3.get_weather()

obs_4 = owm.weather_at_place("San Francisco,USA")
w_4 = obs_4.get_weather()

q_1 = Question(question_text="London,UK", pub_date=timezone.now(),loc=location_1.address,lati=location_1.latitude,long=location_1.longitude,weather=w_1.get_temperature('celsius'))
q_1.save()

q_2 = Question(question_text="New York City,USA", pub_date=timezone.now(),loc=location_2.address,lati=location_2.latitude,long=location_2.longitude,weather=w_2.get_temperature('celsius'))
q_2.save()

q_3 = Question(question_text="Boston,USA", pub_date=timezone.now(),loc=location_3.address,lati=location_3.latitude,long=location_3.longitude,weather=w_3.get_temperature('celsius'))
q_3.save()

q_4 = Question(question_text="San Francisco,USA", pub_date=timezone.now(),loc=location_4.address,lati=location_4.latitude,long=location_4.longitude,weather=w_4.get_temperature('celsius'))
q_4.save()

c_1 = Question.objects.get(pk=1)
c_1.choice_set.create(choice_text="London,UK", loc=location_1.address,lati=location_1.latitude,long=location_1.longitude,weather=w_1.get_temperature('celsius'),votes=0)

c_1.choice_set.create(choice_text="New York City,USA", loc=location_2.address,lati=location_2.latitude,long=location_2.longitude,weather=w_2.get_temperature('celsius'),votes=0)

c_1.choice_set.create(choice_text="Boston,USA", loc=location_3.address,lati=location_3.latitude,long=location_3.longitude,weather=w_3.get_temperature('celsius'),votes=0)

c_1.choice_set.create(choice_text="San Francisco,USA", loc=location_4.address,lati=location_4.latitude,long=location_4.longitude,weather=w_4.get_temperature('celsius'),votes=0)

c_2 = Question.objects.get(pk=2)
c_2.choice_set.create(choice_text="London,UK", loc=location_1.address,lati=location_1.latitude,long=location_1.longitude,weather=w_1.get_temperature('celsius'),votes=0)

c_2.choice_set.create(choice_text="New York City,USA", loc=location_2.address,lati=location_2.latitude,long=location_2.longitude,weather=w_2.get_temperature('celsius'),votes=0)

c_2.choice_set.create(choice_text="Boston,USA", loc=location_3.address,lati=location_3.latitude,long=location_3.longitude,weather=w_3.get_temperature('celsius'),votes=0)

c_2.choice_set.create(choice_text="San Francisco,USA", loc=location_4.address,lati=location_4.latitude,long=location_4.longitude,weather=w_4.get_temperature('celsius'),votes=0)

c_3 = Question.objects.get(pk=3)
c_3.choice_set.create(choice_text="London,UK", loc=location_1.address,lati=location_1.latitude,long=location_1.longitude,weather=w_1.get_temperature('celsius'),votes=0)

c_3.choice_set.create(choice_text="New York City,USA", loc=location_2.address,lati=location_2.latitude,long=location_2.longitude,weather=w_2.get_temperature('celsius'),votes=0)

c_3.choice_set.create(choice_text="Boston,USA", loc=location_3.address,lati=location_3.latitude,long=location_3.longitude,weather=w_3.get_temperature('celsius'),votes=0)

c_3.choice_set.create(choice_text="San Francisco,USA", loc=location_4.address,lati=location_4.latitude,long=location_4.longitude,weather=w_4.get_temperature('celsius'),votes=0)

c_4 = Question.objects.get(pk=4)
c_4.choice_set.create(choice_text="London,UK", loc=location_1.address,lati=location_1.latitude,long=location_1.longitude,weather=w_1.get_temperature('celsius'),votes=0)

c_4.choice_set.create(choice_text="New York City,USA", loc=location_2.address,lati=location_2.latitude,long=location_2.longitude,weather=w_2.get_temperature('celsius'),votes=0)

c_4.choice_set.create(choice_text="Boston,USA", loc=location_3.address,lati=location_3.latitude,long=location_3.longitude,weather=w_3.get_temperature('celsius'),votes=0)

c_4.choice_set.create(choice_text="San Francisco,USA", loc=location_4.address,lati=location_4.latitude,long=location_4.longitude,weather=w_4.get_temperature('celsius'),votes=0)
