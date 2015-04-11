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

for i in range(0, 7):
    today = today + timedelta(1)
    month = str(today.month) 
    day = str(today.day)
    year = str(today.year)
    dayname = week[today.weekday()]

    for location, name  in locations.iteritems():
        url = '''https://campusdining.princeton.edu/dining/_Foodpro/menuSamp.asp?myaction=read&sName=Princeton+UniversityCampus+Dining&dtdate='''+ month+'''%2F'''+day+'''%2F'''+year+'''&locationNum='''+location+'''&naFlag=1'''
        soup = BeautifulSoup(requests.get(url).text)
        hits = soup.body.findAll(text=re.compile(' (W|w)ing'))
        if (hits):
            results.append(dayname + " ("+month+"/"+day+"/"+year+") - " + name)




#! /usr/bin/python

import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# me == my email address
# you == recipient's email address
me = "princetonwings@gmail.com"
recipients = ["tlomont@princeton.edu", "lukel@princeton.edu"]

# Create message container - the correct MIME type is multipart/alternative.
msg = MIMEMultipart('alternative')
msg['Subject'] = "Weekly Wings Update! - " + str(today)
msg['From'] = me
msg['To'] = ", ".join(recipients)

# Create the body of the message (a plain-text and an HTML version).
text = ''
html = """\
<html>
  <head></head>
  <body><h1> This week's wings update!</h1>
"""
for result in results:
    text+= result + "\n"
    html += "<p>" + result + "</p><br>"

html+="""
  </body>
</html>
"""

# Record the MIME types of both parts - text/plain and text/html.
part1 = MIMEText(text, 'plain')
part2 = MIMEText(html, 'html')

# Attach parts into message container.
# According to RFC 2046, the last part of a multipart message, in this case
# the HTML message, is best and preferred.
msg.attach(part1)
msg.attach(part2)

# Send the message via local SMTP server.
server = smtplib.SMTP('smtp.gmail.com:587')
username = 'princetonwings@gmail.com'  
password = os.environ.get('WINGSPASS') 
server.ehlo()
server.starttls()  
server.login(username,password)  
server.sendmail(me, recipients, msg.as_string())         
server.quit()