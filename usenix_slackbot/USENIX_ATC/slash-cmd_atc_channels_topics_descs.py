import slack
import os
import utils.funcs as f
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask, request, Response
from slackeventsapi import SlackEventAdapter

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

app = Flask(__name__)
slack_event_adapter = SlackEventAdapter(
    os.environ['USENIX_SIGNING_SECRET'],'/slack/events',app)

client = slack.WebClient(token=os.environ['USENIX_SLACK_TOKEN'])
BOT_ID = client.api_call("auth.test")['user_id']
user = slack.WebClient(token=os.environ['USENIX_USERSLACK_TOKEN'])

#Initializes slash command /create_channels [link] to create channels in the workspace.
@app.route('/create-channels', methods=['POST'])
def create_channels():
    data = request.form
    weblink = request.form.get('text')
    user_id = data.get('user_id')
    channel_id = data.get('channel_id')
    list_of_channels = list(f.slack_channels_atc(weblink))
    client.chat_postMessage(channel=channel_id, text='{} channels requested. Please wait.'.format(len(list_of_channels)))

    #Creates a list of channels already in the workspace and checks them against the requested channels list.
    existing_channels = client.conversations_list(limit=999)
    total_channels = len(existing_channels["channels"])
    counter = 0
    list_of_total_channels = []
    
    while counter < total_channels:
        list_of_total_channels.append(existing_channels["channels"][counter]["name"])
        counter+=1

    #Iterates over the channels and creates new public channels if they are not already in the workspace.
    for channel_to_add in list_of_channels:
        if channel_to_add not in list_of_total_channels:
            client.conversations_create(name=channel_to_add)
            client.chat_postMessage(channel=channel_id, text='Created new channel {}'.format(channel_to_add))
        else:
            client.chat_postMessage(channel=channel_id, text='{} already exists!'.format(channel_to_add))
            continue
    
    client.chat_postMessage(channel=channel_id, text='Channels created. Please use the /set-topic-desc command with the same weblink to update the topics and descriptions for each channel.')

    return Response(), 200

#Initializes slash command /set_topic_desc [link] to set the topics and descriptions of the channels created from /create_channels.
@app.route('/set-topic-desc', methods=['POST'])
def set_topic_desc():
    data = request.form
    weblink = request.form.get('text')
    user_id = data.get('user_id')
    channel_id = data.get('channel_id')
    client.chat_postMessage(channel=channel_id, text='Received request. Updating topics and descriptions. Note that topic and description updates will appear as set by Livi. Please wait, this may take a moment.')
    new_channels = list(f.slack_channels_atc(weblink))
    existing_channels = client.conversations_list(limit=999)
    counter = 0
    channel_ids = []
    channel_names = []
    
    #Creates a hashmap of channel ids to names.
    while counter < len(existing_channels["channels"]):
        channel_ids.append(existing_channels["channels"][counter]["id"])
        channel_names.append(existing_channels["channels"][counter]["name"])
        counter += 1
    
    all_names_ids = dict(zip(channel_names, channel_ids))
    names_ids = {x: all_names_ids[x] for x in new_channels}
    
    #Ensures the user has joined the channels.
    for key, val in names_ids.items():
        user.conversations_join(channel=val)
    
    #Collects topic and descriptions in lists.
    topic_strings = list(f.channel_topic_atc(weblink))
    desc_strings = list(f.channel_desc_atc(weblink))

    for key, value in names_ids.items():
        names_ids[key]=[value]
        
    #Maps IDs to topics and descriptions.
    y = 0
    for key, val in names_ids.items():
        names_ids[key].append(topic_strings[y])
        names_ids[key].append(desc_strings[y])
        y += 1
    
    #Set the corresponding topic and description to each channel.
    for key, val in names_ids.items():
        user.conversations_setTopic(channel=names_ids[key][0], topic=names_ids[key][1])
        user.conversations_setPurpose(channel=names_ids[key][0], purpose=names_ids[key][2])

    client.chat_postMessage(channel=channel_id, text='Successfully updated topics and descriptions.')

    return Response(), 200

if __name__ == "__main__":
    app.run(debug=True)
