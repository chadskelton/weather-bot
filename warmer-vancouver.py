#!/usr/bin/env python

# This is set on a schedule in ScraperWiki to run once a day

import scraperwiki
import tweepy
import time
from datetime import datetime
import smtplib
import requests
from BeautifulSoup import BeautifulSoup
import random
import datetime

# Establish Twitter authorization.
# Need to sign up for API key at dev.twitter.com and connect your bot to a mobile phone so you can post through the API

TWEEPY_CONSUMER_KEY = 'YOUR_API_KEY'
TWEEPY_CONSUMER_SECRET = 'YOUR_API_KEY'
TWEEPY_ACCESS_TOKEN = 'YOUR_API_KEY'
TWEEPY_ACCESS_TOKEN_SECRET = 'YOUR_API_KEY'

auth1 = tweepy.auth.OAuthHandler(TWEEPY_CONSUMER_KEY, TWEEPY_CONSUMER_SECRET)
auth1.set_access_token(TWEEPY_ACCESS_TOKEN, TWEEPY_ACCESS_TOKEN_SECRET)
api = tweepy.API(auth1)

url = "http://weather.gc.ca/canada_e.html" # list of current temperature in Canadian cities

html = requests.get(url)
htmlpage = html.content

soup = BeautifulSoup(htmlpage)

table = soup.find ("tbody")

rows = table.findAll ("tr")

for row in rows:
    cells = row.findAll ("td")
    city = cells[0].text
    rawdegrees = cells[2].text
    degrees = int(rawdegrees.replace('&deg;C',''))
    if 'Vancouver' in city:
        vancouvertemp = degrees # finds current Vancouver temperature, saves it

record = []

recordlist = []

for row in rows:
    cells = row.findAll ("td")
    city = cells[0].text
    rawdegrees = cells[2].text
    degrees = int(rawdegrees.replace('&deg;C','')) # gets rid of weird degree formatting in temperatures
    if degrees < vancouvertemp:
        record = []
        if "Ottawa" in city:
            city = "Ottawa" # reformats "Ottawa (Kanata - Orleans)" as simply "Ottawa"
        record.append(city)
        record.append(degrees)
        record.append(vancouvertemp - degrees)
        recordlist.append(record)
        
print recordlist

choice = random.choice(recordlist) # randomly choose from all cities colder than Vancouver
    
print choice

amount = ""

# the code below changes the language of the tweet based on how much colder the randomly chosen temperature is to Vancouver

if choice[2] > 0:
    amount = "a tiny bit"
if choice[2] > 2:
    amount = "a little bit"
if choice[2] > 5:
    amount = "quite a bit"
if choice[2] > 10:
    amount = "a lot"
if choice[2] > 20:
    amount = "waaay"
if choice[2] > 30:
    amount = "ridiculously"
    
statusupdate = "It's " + amount + " warmer in Vancouver right now (" + str(vancouvertemp) + "C) than in " + choice[0] + " (" + str(choice[1]) + "C). " # creates tweet text

print statusupdate

api.update_status(statusupdate) # tweets out tweet text
