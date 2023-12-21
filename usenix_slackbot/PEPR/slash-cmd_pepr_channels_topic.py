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
    os.environ['SIGNING_SECRET'],'/slack/events',app)

client = slack.WebClient(token=os.environ['PEPR_SLACK_TOKEN'])
BOT_ID = client.api_call("auth.test")['user_id']
user = slack.WebClient(token=os.environ['PEPR_USERSLACK_TOKEN'])

#Initializes slash command /create_channels [link] to create channels in the workspace.
@app.route('/create-channels', methods=['POST'])
def create_channels():
    data = request.form
    weblink = request.form.get('text')
    user_id = data.get('user_id')
    channel_id = data.get('channel_id')
    list_of_channels = list(f.slack_channels_pepr(weblink))
    client.chat_postMessage(channel=channel_id, text='{} channels requested. Please wait.'.format(len(list_of_channels)))

    #Creates a list of channels already in the workspace and checks them against the requested channels list.
    existing_channels = client.conversations_list()
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

    #Creates a hashmap of channel ids to channel names.
    new_channels = list(f.slack_channels_pepr(weblink))
    counter = 0
    existing_channels = client.conversations_list()
    channel_ids = []
    channel_names = []
    
    while counter < len(existing_channels["channels"]):
        channel_ids.append(existing_channels["channels"][counter]["id"])
        channel_names.append(existing_channels["channels"][counter]["name"])
        counter += 1
    
    all_names_ids = dict(zip(channel_names, channel_ids))
    names_ids = {x: all_names_ids[x] for x in new_channels}

    #Adds user using slash command to the channels being requested.
    for id in channel_ids:
        client.chat_postMessage(channel=channel_id, text='Adding you to all channels.')
        user.conversations_join(channel=id)
        client.chat_postMessage(channel=channel_id, text='Successfully added.')

    return Response(), 200

if __name__ == "__main__":
    app.run(debug=True)
