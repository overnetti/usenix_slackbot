import os
import sys
import requests
import time
import urllib.request
from bs4 import BeautifulSoup
from bs4.element import Comment
from urllib.request import urlopen

def slack_channels_osdi(body):
  soup = BeautifulSoup(urlopen(body))
  
  #Retrieves bulk of text from the page to work with.
  days_tracks = [x.getText() for x in soup.findAll('div',{'class':'field-items'})] 
  days_tracks_1 = list(filter(None, days_tracks)) 
  titles_raw = [x.getText() for x in soup.findAll('h2')] 
  h2_titles = []
  
  for x in titles_raw:
    if not x.startswith('\n'):
      h2_titles.append(x) 
  
  #Retrieves session titles.
  session_titles_raw = [x.getText() for x in soup.findAll('h2',{'class':'node-title'})] 
  session_titles_clean = [x for x in session_titles_raw if not x.startswith('\n')] 
  cleaned_days = [x.replace('\n', '') for x in days_tracks_1] 
  formatted_list = [] 
  
  for x in cleaned_days:
    if x == 'Continental Breakfast':
      formatted_list.append(x) 
  
  h = 0
  i = 0
  j = 1
  ch_list = []
  
  #Gets the conference name to add to the channel names.
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
  
  i = 0
  
  while i < len(days_split):
    if days_split[i] == 'January':
        days_split[i] = '01'
    if days_split[i] == 'February':
        days_split[i] = '02'
    if days_split[i] == 'March':
        days_split[i] = '03'
    if days_split[i] == 'April':
        days_split[i] = '04'
    if days_split[i] == 'May':
        days_split[i] = '05'
    if days_split[i] == 'June':
        days_split[i] = '06'
    if days_split[i] == 'July':
        days_split[i] = '07'
    if days_split[i] == 'August':
        days_split[i] = '08'
    if days_split[i] == 'September':
        days_split[i] = '09'
    if days_split[i] == 'October':
        days_split[i] = '10'
    if days_split[i] == 'November':
        days_split[i] = '11'
    if days_split[i] == 'December':
        days_split[i] = '12'
    if days_split[i] == '1':
        days_split[i] = '01'
    if days_split[i] == '2':
        days_split[i] = '02'
    if days_split[i] == '3':
        days_split[i] = '03'
    if days_split[i] == '4':
        days_split[i] = '04'
    if days_split[i] == '5':
        days_split[i] = '05'
    if days_split[i] == '6':
        days_split[i] = '06'
    if days_split[i] == '7':
        days_split[i] = '07'
    if days_split[i] == '8':
        days_split[i] = '08'
    if days_split[i] == '9':
        days_split[i] = '09'
    i += 1
  
  days = [] 
  
  for x in days_split:
    if x.endswith('y'):
      days.append(x) 
      days_split.remove(x) 
  
  list_length = len(days_split)
  dates = [days_split[i] + days_split[i+1] for i in range(0, list_length-1, 2)]
  i = 0
  j = 0
  parser_list = []
  
  for x in session_titles_clean:
    parser_list.append(x)
  
  for x in extract_days:
    parser_list.append(x)
  
  days_sessions_in_order = []
  
  for x in h2_titles:
    if x in parser_list:
      days_sessions_in_order.append(x)
  
  #Compiles days and their sessions.
  days_sessions_in_order_cleaned = [x.split(',')[0] for x in days_sessions_in_order]
  
  for x in days_sessions_in_order_cleaned:
    if 'Keynote' in x:
      days_sessions_in_order_cleaned.remove(x)
  
  days_sessions_dashes = [x.replace(' ','-') for x in days_sessions_in_order_cleaned] 
  formatted_with_sessions = []
  counter = 0
  
  for x in days_sessions_dashes:
    if 'day' in x:
        counter = 0
    else:
        if not 'day' in x:
          counter += 1
        formatted_with_sessions.append(f's{counter}') 
    formatted_with_sessions.append(x)
  
  key = None
  
  #Maps days to their sessions and titles.
  days_sessions_titles = dict()
  
  for x in formatted_with_sessions:
    if 'day' in x:
      key = x
      days_sessions_titles[key] = []
    else:
      days_sessions_titles[key].append(x)
  
  if list_length % 2 == 1:
    dates.append(days_split[list_length-1])
  
  days_dates = dict()
  
  for key, val in zip(days, dates):
    days_dates[key] = val
  
  for key, values in days_sessions_titles.items():
    if(isinstance(values, list)):
      session = [x for x in values[0:len(values):2]]
      session_titles = [x.lower() for x in values[1:len(values):2]]
      counter = 0
    
    #Generates channels in the specific format. 
    while counter<len(session):
      yield conf_title_strings_clean[1].lower()+'-'+conf_title_strings_clean[0].lower()+'-'+days_dates[key]+'-'+session[counter]
      counter += 1


#Creates the topics for each channel.
def channel_topic_osdi(body):
  soup = BeautifulSoup(urlopen(body))
  
  #Gets the sessions and their titles.
  session_titles_raw = [x.getText() for x in soup.findAll('h2',{'class':'node-title'})] 
  session_titles_clean = [x for x in session_titles_raw if not x.startswith('\n')] 
  
  for x in session_titles_clean:
    if 'Keynote' in x:
      session_titles_clean.remove(x)
  
  #Gets the conference title and splits it up into separate strings in a list.
  substring = 'Technical Sessions\n'
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
def channel_desc_osdi(body):
  soup = BeautifulSoup(urlopen(body))
  
  #Gets the conference title and splits it up into separate strings in a list.
  substring = 'Technical Sessions\n'
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
  
  for x in session_titles_clean:
    if 'Keynote' in x:
      session_titles_clean.remove(x)
  
  h2_titles = [] 
  
  for x in titles_raw:
    if not x.startswith('\n'):
      h2_titles.append(x)
  
  #Gets and formats the days and session titles.
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
  
  size = len(days_sessions_in_order)
  idx_list = [idx for idx, val in enumerate(days_sessions_in_order) if 'day' in val]
  res = [days_sessions_in_order[i: j] for i, j in zip([0] + idx_list, idx_list + ([size] if idx_list[-1] != size else []))]
  final_res = [x for x in res if x]
  days_sessions = {}
  
  #Maps days to sessions.
  for x in final_res:
      key, value = x[0], x[1:]
      days_sessions[key] = value
  
  #Formats the descriptions.
  for key, values in days_sessions.items():
    for value in values:
      yield "Session Q&A for '"+str(value)+"' - "+conf_title_strings[0]+" "+conf_title_strings[1]+" "+"("+str(key)+")"
