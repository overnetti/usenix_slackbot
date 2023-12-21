# Slackbot for USENIX Workspace set-up

## Introduction
The python script `slack_slashcmd_channels_topics_descs.py` scrapes the technical sessions pages of USENIX events in order to create uniquely formatted channels, topics, and descriptions in a specific Slack event workspace.

This script is one of many iterations of this Slackbot. 

The USENIX Association is an advanced computing systems nonprofit organization, known for organizing conferences and publishing research. This Slackbot served the following of their events: Enigma, FAST, NSDI, PEPR, USENIX ATC, OSDI, SOUPS, and USENIX Security.

Datasources:
- Program page or Technical Sessions page links. Example: https://www.usenix.org/conference/usenixsecurity22/technical-sessions

## Need to Know

- Expected execution time: around 1 to 3 minutes depending on size of program/technical sessions.
- User will need to use the slash commands in a DM with the bot for the program to execute.
- If the channel already exists, the bot will print out the channel name and let the user know it exists before skipping it.
- Slackbot will need to be set up in the workspace and will need to be allowed permissions to read messages, write messages, create channels, and update topics and descriptions.


## Guidelines

#### Execution

1. 

#### Execute from IDE or Command line (only for development purposes)

1. 
