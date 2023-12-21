# Slackbot for USENIX Workspace set-up

## Introduction
This Slackbot scrapes the technical sessions pages or program pages of specific USENIX events in order to create uniquely formatted channels, topics, and descriptions in a specific Slack event workspace. This bot was created for the USENIX Association, an advanced computing systems nonprofit organization, known for organizing conferences and publishing research. This Slackbot served the following of their events: NSDI, PEPR, USENIX ATC, OSDI, SOUPS, and USENIX Security. Prior to this bot, the task of setting up the event workspace for a conference was assigned to a team member for completion within 2 weeks. Team members have to compile the data from the program pages or technical sessions pages manually and copy-paste the information into a Google Sheet. The data is concatenated to create channels, topics, and descriptions and team members copy-paste this information one by one into the workspace. The process is tedious, as the topics and descriptions can only be added once the channel is created. This project saves the USENIX team ~400 hours of manual labor annually by automating the process.

Datasources:
- Program page or Technical Sessions page links. Example: https://www.usenix.org/conference/usenixsecurity22/technical-sessions

## Need to Know

- Expected execution time: around 1 to 3 minutes depending on size of program/technical sessions.
- User will need to use the slash commands in a DM with the bot for the program to execute.
- If the channel already exists, the bot will print out the channel name and let the user know it exists before skipping it.
- Slackbot will need to be set up in the workspace and will need to be allowed permissions to read messages, write messages, create channels, and update topics and descriptions.
- This project does not include the .env file and will need to be created.


## Guidelines

#### Slackbot Set-up
1. Visit api.slack.com and click Your apps in the top right corner to sign in.
2. Click Create an app.
3. Select **From scratch** and name the bot.
4. Click **Bots** under **Add features and functionality** header.
5. Click **Review scopes to add** and scroll to **Bot token scopes**
6. Add the following scopes: **channels:read**, **conversations:write.topic**, **conversations:write.invites**, **admin.conversations:read**, **admin.conversations:write**, **channels:history**, **channels:join**, **channels:manage**, **channels:read**, **channels:write**, **channels:write.invites**, **chat:write**, **chat:write.customize**, and **chat:write.public**
7. Scroll up and click **Install to workspace** and **Allow** on the following screen.
8. Your **Bot User OAuth Token** should now be visible. Copy and paste this into your .env file.
9. Lastly, add the Bot to at least one channel by running the command **/invite @<Botname>**

For more information, visit: https://medium.com/applied-data-science/how-to-build-you-own-slack-bot-714283fd16e5

#### Execution

1. 

#### Dependencies for development purposes

1. Python 3.8 or later
2. ngrok: https://ngrok.com/download
3. `pip install slack`
4. `pip install os`
5. `pip install pathlib`
6. `pip install python-dotenv`
7. `pip install flask`
8. `pip install slackeventsapi`
9. `pip install sys`
10. `pip install requests`
11. `pip install time`
12. `pip install urllib.request`
13. `pip install bs4`
