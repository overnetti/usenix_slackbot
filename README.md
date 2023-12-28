# Slackbot for USENIX Workspace set-up

## Introduction

This is a replicated copy of my work at USENIX. This does not accurately represent private data at USENIX.

This Slackbot scrapes the technical sessions pages or program pages of specific USENIX events in order to create uniquely formatted channels, topics, and descriptions in a specific Slack event workspace. This bot was created for the USENIX Association, an advanced computing systems nonprofit organization, known for organizing conferences and publishing research. This Slackbot served the following of their events: NSDI, PEPR, USENIX ATC, OSDI, SOUPS, and USENIX Security. Prior to this bot, the task of setting up the event workspace for a conference was assigned to a team member for completion within 2 weeks. Team members have to compile the data from the program pages or technical sessions pages manually and copy-paste the information into a Google Sheet. The data is concatenated to create channels, topics, and descriptions and team members copy-paste this information one by one into the workspace. The process is tedious, as the topics and descriptions can only be added once the channel is created. This project saves the USENIX team ~400 hours of manual labor annually by automating the process.

Datasources:
- Program page or Technical Sessions page links. Example: https://www.usenix.org/conference/usenixsecurity22/technical-sessions

## Need to Know

- Expected execution time: around 1 to 3 minutes depending on size of program/technical sessions.
- User will need to use the slash commands in a DM with the bot for the program to execute.
- If the channel already exists, the bot will print out the channel name and let the user know it exists before skipping it.
- Slackbot will need to be set up in the workspace and will need to be allowed permissions to read messages, write messages, create channels, and update topics and descriptions.
- The bot has only ever ran on a local ngrok server.
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

1. Launch ngrok by running the following command in the terminal: `ngrok http 3000`
2. Copy the URL in **Forwarding** (up until the .io)
3. Navigate to your app in api.slack.com
4. Navigate to the **Event Subscriptions** page and click the **Enable Events** slider to turn it on.
5. In the **Request** URL field, enter the URL provided by ngrok to expose your application to the internet.
6. In the left menu, click **Install App**, click **Install to Workspace**, and click **Allow**. The bot will need to be re-installed to the workspace each time updates like these are made.
7. Now, return to the Terminal and navigate to the location of the python file that begins with `slash-cmd` for the specific event of interest.
8. Run the file that begins with `slash-cmd`. A server should boot up on your Terminal and the slash command for the specific event can now be used in a DM with the bot by users in the workspace.
9. Open a DM with the bot and type **/create_channels [link_to_program_pg]** to run the channel creation script. Type **/set_topic_desc [link_to_program_pg]** to set the topics and descriptions for each channel.

#### Dependencies

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

## Future Improvements
1. Project should be hosted on the cloud instead of locally, so that the service is always available for team members to use.
2. Data could be compiled into a SQL database with web scraping and stored for bot usage.
3. Bot should determine which iteration of itself to use based on conference link received.
4. If the bot is being continuously hosted on a server, further features could be added like listening to specific events and alerting staff.
