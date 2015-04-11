from time import strftime, localtime
from datetime import date, timedelta
from bs4 import BeautifulSoup
import requests
import re
import os

results = []

week   = ['Monday', 
              'Tuesday', 
              'Wednesday', 
              'Thursday',  
              'Friday', 
              'Saturday',
              'Sunday',]

locations = {'02':'Butler/Wilson', '03':'Forbes', '01':'Rockey/Mathey', '08':'Whitman'}

today = date.today()
month = str(today.month) 
day = str(today.day)
year = str(today.year)
dayname = week[today.weekday()]
hour = strftime("%H", localtime())

if (dayname == 'Saturday' or 'Sunday'):
    if (hour == '10'):
        mealindex = 0
    else:
        mealindex = 1
        
else:
    if (hour == '10'):
        mealindex = 0
    elif (hour == '11'):
        mealindex = 1
    else:
        mealindex = 2

for location, name  in locations.iteritems():
    url = '''https://campusdining.princeton.edu/dining/_Foodpro/menuSamp.asp?myaction=read&sName=Princeton+UniversityCampus+Dining&dtdate='''+ month+'''%2F'''+day+'''%2F'''+year+'''&locationNum='''+location+'''&naFlag=1'''
    soup = BeautifulSoup(requests.get(url).text)
    a = soup.findAll("tr", height="5")
    hits = a[mealindex].findAll(text=re.compile(' (W|w)ing'))
    if (hits):
        results.append(location)


#send the yo

for location in results:
    url = '''https://campusdining.princeton.edu/dining/_Foodpro/menuSamp.asp?myaction=read&sName=Princeton+UniversityCampus+Dining&dtdate='''+ month+'''%2F'''+day+'''%2F'''+year+'''&locationNum='''+location+'''&naFlag=1'''
    requests.post('http://api.justyo.co/yoall', data={'api_token': os.environ.get("YOKEY"),'link': url}) # Send Yo to all