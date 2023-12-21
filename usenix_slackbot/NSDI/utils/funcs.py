import os
import sys
import requests
import time
import urllib.request
from bs4 import BeautifulSoup
from bs4.element import Comment
from urllib.request import urlopen

def slack_channels_nsdi(body):
  soup = BeautifulSoup(urlopen(body), features="html.parser")
  
  #Retrieves bulk of text from the page to work with.
  days_tracks = [x.getText() for x in soup.findAll('div',{'class':'field-items'})]
  days_tracks_1 = list(filter(None, days_tracks))
  cleaned_days_tracks = [x.replace('\n', '') for x in days_tracks_1]
  formatted_list = []
  
  for x in cleaned_days_tracks:
    if x == 'Continental Breakfast':
      formatted_list.append(x)
    elif x == 'Morning Coffee and Tea':
      formatted_list.append(x)
    if x == 'Track 1':
      formatted_list.append(x)
    if x == 'Track 2':
      formatted_list.append(x)
    if x == 'Track 3':
      formatted_list.append(x)
  
  #Gets the conference name to add to the channel names.
  h = 0
  i = 0
  j = 1
  ch_list = []
  substring = 'Technical Sessions\n'
  extract_conf = [x.getText() for x in soup.findAll('div',{'class':'outer-wrapper'})]
  raw_conf_title = [x for x in extract_conf if substring in x]
  conf_title_clean = [x.replace('\n', '') for x in raw_conf_title]
  conf_title_strings = []
  
  for x in conf_title_clean:
    conf_title_strings.extend(x.split())
  
  conf_title_strings_clean = [x.replace("'","") for x in conf_title_strings]
  
  #Gets the order of days and times for dating format in the channel names.
  extract_days_times = [x.getText() for x in soup.findAll('span',{'class':'field-item odd first last'})]
  extract_days = []
  
  for x in extract_days_times:
    if x.startswith(('Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday')):
      extract_days.append(x)
  
  days_without_commas = [x.replace(',','') for x in extract_days]
  days_split = []
  
  for x in days_without_commas:
    days_split.extend(x.split())
  
  days_clean = [x for x in days_split if not x.startswith('20')]
  
  i = 0
  
  while i < len(days_clean):
    if days_clean[i] == 'January':
        days_clean[i] = '01'
    if days_clean[i] == 'February':
        days_clean[i] = '02'
    if days_clean[i] == 'March':
        days_clean[i] = '03'
    if days_clean[i] == 'April':
        days_clean[i] = '04'
    if days_clean[i] == 'May':
        days_clean[i] = '05'
    if days_clean[i] == 'June':
        days_clean[i] = '06'
    if days_clean[i] == 'July':
        days_clean[i] = '07'
    if days_clean[i] == 'August':
        days_clean[i] = '08'
    if days_clean[i] == 'September':
        days_clean[i] = '09'
    if days_clean[i] == 'October':
        days_clean[i] = '10'
    if days_clean[i] == 'November':
        days_clean[i] = '11'
    if days_clean[i] == 'December':
        days_clean[i] = '12'
    if days_clean[i] == '1':
        days_clean[i] = '01'
    if days_clean[i] == '2':
        days_clean[i] = '02'
    if days_clean[i] == '3':
        days_clean[i] = '03'
    if days_clean[i] == '4':
        days_clean[i] = '04'
    if days_clean[i] == '5':
        days_clean[i] = '05'
    if days_clean[i] == '6':
        days_clean[i] = '06'
    if days_clean[i] == '7':
        days_clean[i] = '07'
    if days_clean[i] == '8':
        days_clean[i] = '08'
    if days_clean[i] == '9':
        days_clean[i] = '09'
    i += 1
  
  days = []
  
  for x in days_clean:
    if x.endswith('y'):
      days.append(x)
      days_clean.remove(x)
  
  i = 0
  j = 0
  
  #Uses the breakfast session to determine a new day.
  while i < len(formatted_list):
    if formatted_list[i] == 'Continental Breakfast':
      formatted_list[i] = days[j]
      j+=1
    i += 1
  
  formatted_with_sessions = []
  
  for x in formatted_list:
    if 'day' in x:
        counter = 0
    else:
        if 'Track 1' in x:
            counter +=1
        formatted_with_sessions.append(f's{counter}')
    formatted_with_sessions.append(x)
  
  i = 0
  
  while i < len(formatted_with_sessions):
    if formatted_with_sessions[i] == 'Track 1':
      formatted_with_sessions[i] = 't1'
    if formatted_with_sessions[i] == 'Track 2':
      formatted_with_sessions[i] = 't2'
    if formatted_with_sessions[i] == 'Track 3':
      formatted_with_sessions[i] = 't3'
    if formatted_with_sessions[i] == 'Track 4':
      formatted_with_sessions[i] = 't4'
    i += 1
  
  #Maps days to sessions and their tracks.
  key = None
  days_sessions_tracks = dict()
  
  for x in formatted_with_sessions:
    if 'day' in x:
      key = x
      days_sessions_tracks[key] = []
    else:
      days_sessions_tracks[key].append(x)
  
  trial_list = []
  list_length = len(days_clean)
  dates = [days_clean[i] + days_clean[i+1] for i in range(0, list_length-1, 2)]
  
  if list_length % 2 == 1:
    dates.append(days_clean[list_length-1])
  
  days_dates = dict()
  
  for key, val in zip(days, dates):
    days_dates[key] = val
  
  for key, values in days_sessions_tracks.items():
    if(isinstance(values, list)):
      track = [x for x in values[0:len(values):2]]
      session = [x for x in values[1:len(values):2]]
      counter = 0
    
    #Generates channels in the specific format. 
    while counter < len(track):
      yield conf_title_strings_clean[1].lower()+'-'+conf_title_strings_clean[0].lower()+'-'+days_dates[key]+'-'+track[counter]+'-'+session[counter]
      counter += 1
