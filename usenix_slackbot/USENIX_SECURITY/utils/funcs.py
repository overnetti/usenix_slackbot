import os
import sys
import json
import requests
import time
import re
import urllib.request
from bs4 import BeautifulSoup
from bs4.element import Comment
from urllib.request import urlopen

#Creates and formats sessions and tracks into channels for Slack workspace.
def slack_channels_sec(body):
  soup = BeautifulSoup(urlopen(body), features="html.parser")
  
  #Retrieves bulk of text from the page to work with.
  days_tracks = [x.getText() for x in soup.findAll('div',{'class':'field-items'})] 
  days_tracks_1 = list(filter(None, days_tracks)) 
  session_titles_raw = [x.getText() for x in soup.findAll('h2',{'class':'node-title'})] 
  session_titles_clean = [x for x in session_titles_raw if not x.startswith('\n')] 
  extract_days_times = [x.getText() for x in soup.findAll('span',{'class':'field-item odd first last'})] 
  extract_days = []
  
  for x in extract_days_times:
    if x.startswith(('Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday')):
      extract_days.append(x)
      
  cleaned_days_tracks = [x.replace('\n', '') for x in days_tracks_1]
  titles_raw = [x.getText() for x in soup.findAll('h2')]
  
  h2_titles = [] 
  
  for x in titles_raw:
    if not x.startswith('\n'):
      h2_titles.append(x)
      
  formatted_list = []
  h2_parser = []
  
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
    if x == 'Track 4':
      formatted_list.append(x)
  
  for x in session_titles_clean:
    h2_parser.append(x)
  
  for x in extract_days:
    h2_parser.append(x)
  
  #Places days and sessions in order.
  days_sessions_in_order = []
  
  for x in h2_titles:
    if x in h2_parser:
      days_sessions_in_order.append(x)
  
  for x in days_sessions_in_order:
    if 'Keynote' in x:
      days_sessions_in_order.remove(x)
  formatted_days_sessions_in_order = []
  
  for x in days_sessions_in_order:
    y = x.lower().replace(' ', '-')
    formatted_days_sessions_in_order.append(y)
  
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
  
  for x in conf_title_strings_clean:
    if 'USENIX' in x:
      conf_title_strings_clean.remove(x)
  
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
  
  len_days_tracks = len(formatted_list)
  len_days_sessions = len(formatted_days_sessions_in_order)
  formatted_with_sessions = []
  
  for x in formatted_list:
    if 'day' in x:
        counter = 0
    else:
        if 'Track 1' in x: 
          counter += 1
        formatted_with_sessions.append(f's{counter}')
    formatted_with_sessions.append(x)
  
  #Formats tracks.
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
  
  #Maps the days to the sessions and tracks.
  h = 0
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
      yield conf_title_strings_clean[0][0:3].lower()+conf_title_strings_clean[1].lower()+'-'+days_dates[key]+'-'+track[counter]+'-'+session[counter]
      counter += 1


#Creates the topics for each channel.
def channel_topic_sec(body):
  soup = BeautifulSoup(urlopen(body), features="html.parser")
  
  #Gets the sessions and their titles.
  session_titles_raw = [x.getText() for x in soup.findAll('h2',{'class':'node-title'})] 
  session_titles_clean = [x for x in session_titles_raw if not x.startswith('\n')] 
  
  for x in session_titles_clean:
    if 'Keynote' in x:
      session_titles_clean.remove(x)
      
  substring = 'Technical Sessions\n'
  
  #Gets the conference title and splits it up into separate strings in a list.
  extract_conf = [x.getText() for x in soup.findAll('div',{'class':'outer-wrapper'})] 
  raw_conf_title = [x for x in extract_conf if substring in x] 
  conf_title_clean = [x.replace('\n', '') for x in raw_conf_title]
  conf_title_strings = []
  
  for x in conf_title_clean:
    conf_title_strings.extend(x.split())
  
  #Formats the data in a specific string for each topic. 
  for x in session_titles_clean:
    yield "'"+x+"' - session Q&A ("+conf_title_strings[0]+" "+conf_title_strings[1]+")"


#Creates the descriptions for each channel.
def channel_desc_sec(body):
  soup = BeautifulSoup(urlopen(body), features="html.parser")
  substring = 'Technical Sessions\n'
  
  #Gets the conference title and splits it up into separate strings in a list.
  extract_conf = [x.getText() for x in soup.findAll('div',{'class':'outer-wrapper'})] 
  raw_conf_title = [x for x in extract_conf if substring in x] 
  conf_title_clean = [x.replace('\n', '') for x in raw_conf_title] 
  conf_title_strings = []
  
  for x in conf_title_clean:
    conf_title_strings.extend(x.split())
  
  #Gets the session titles.
  session_titles_raw = [x.getText() for x in soup.findAll('h2',{'class':'node-title'})] 
  session_titles_clean = [x for x in session_titles_raw if not x.startswith('\n')] 
  titles_raw = [x.getText() for x in soup.findAll('h2')] 
  
  #Gets and formats the days, tracks, and session titles.
  days_tracks = [x.getText() for x in soup.findAll('div',{'class':'field-items'})] 
  days_tracks_1 = list(filter(None, days_tracks)) 
  cleaned_days_tracks = [x.replace('\n', '') for x in days_tracks_1] 
  formatted_list = []
  
  for x in cleaned_days_tracks:
    if x == 'Track 1':
      formatted_list.append(x)
    if x == 'Track 2':
      formatted_list.append(x)
    if x == 'Track 3':
      formatted_list.append(x)
    if x == 'Track 4':
      formatted_list.append(x)
  
  for x in session_titles_clean:
    if 'Keynote' in x:
      session_titles_clean.remove(x)
  
  h2_titles = [] 
  
  for x in titles_raw:
    if not x.startswith('\n'):
      h2_titles.append(x)
  
  extract_days_times = [x.getText() for x in soup.findAll('span',{'class':'field-item odd first last'})] 
  extract_days = [] 
  
  for x in extract_days_times:
    if x.startswith(('Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday')):
      extract_days.append(x)
  
  parser_list = []
  for x in session_titles_clean:
    parser_list.append(x)
  
  for x in extract_days:
    parser_list.append(x)
  
  days_sessions_in_order = []
  for x in h2_titles:
    if x in parser_list:
      days_sessions_in_order.append(x)
  
  day_sesh_track_order = []
  for i in range(len(days_sessions_in_order)):
    try:
        day_sesh_track_order.append(days_sessions_in_order[i])
        day_sesh_track_order.append(formatted_list[i])
    except IndexError:
        continue
  
  tracks_lst = []
  
  for x in formatted_list:
    if x not in tracks_lst:
      tracks_lst.append(x)
  
  insertcounter = 0
  counter_day = 0
  counter_track = 0
  days_and_tracks = []
  
  while i < len(days_sessions_in_order):
      if counter_day == i:
          i += i
      text = days_sessions_in_order[counter_day]
      if (re.search("Monday", text) or re.search("Tuesday", text) or re.search("Wednesday", text) or re.search("Thursday", text) or re.search("Friday", text)):
          days_and_tracks.insert(insertcounter, text)
          insertcounter += 1
      else:
          track = text + " " + formatted_list[counter_track]
          track = "("+formatted_list[counter_track]+")"
          track_day = text+" "+track
          days_and_tracks.insert(insertcounter, track_day)
          insertcounter += 1
          counter_track += 1
      counter_day += 1
  
  days_sessions_in_order = days_and_tracks
  idxcounter = 0
  size = len(days_sessions_in_order)
  idx_list = [idx for idx, val in enumerate(days_sessions_in_order) if 'day' in val]
  res = [days_sessions_in_order[i: j] for i, j in zip([0] + idx_list, idx_list + ([size] if idx_list[-1] != size else []))]
  final_res = [x for x in res if x]
  
  #Maps days to sessions.
  days_sessions = {}
  
  for x in final_res:
      key, value = x[0], x[1:]
      days_sessions[key] = value
  
  counter = 0
  insertcounter = 0
  sesh_length = len(days_sessions[key])
  
  #Formats the descriptions.
  for key, values in days_sessions.items():
    for value in values:
      yield "Session Q&A for "+str(value)+" - "+conf_title_strings[0]+" "+conf_title_strings[1]+" "+"("+str(key)+")"

