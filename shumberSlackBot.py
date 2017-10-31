import os
import time
from slackclient import SlackClient
from dotenv import load_dotenv

load_dotenv('keys.env')

slack_token = os.environ['SLACK_API_TOKEN']
sc = SlackClient(slack_token)

sc.api_call(
  "chat.postMessage",
  channel="#bot_playground",
  text="Hello from scottSlackBot! :tada:"
)

if sc.rtm_connect(): #connect to slack 
    while True:
        event = sc.rtm_read()
        print(event)

        time.sleep(1)
else:
    print("Connection Failed")

#create list of users
#determin when a user joins and leaves a channel
#create a command to send a user a message