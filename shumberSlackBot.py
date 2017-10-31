import os
import time
from slackclient import SlackClient
from dotenv import load_dotenv

load_dotenv('keys.env')

slack_token = os.environ['SLACK_API_TOKEN']
sc = SlackClient(slack_token)
'''
sc.api_call(
  "chat.postMessage",
  channel="#bot_playground",
  text="Hello from scottSlackBot! :tada:"
)
'''
userList = {}
if sc.rtm_connect(): #connect to slack 
    api_call = sc.api_call("users.list")
    users = api_call.get('members')
    for user in users:
        userList[user['id']] = {}
        userList[user['id']]['active'] = 0
        userList[user['id']]['away'] = 0
        userList[user['id']]['total'] = 0
    while True:
        event = sc.rtm_read()
        #print(event)
        if event['type'] == "presence_change":
            handlePresenceChange(event)
        time.sleep(1)
else:
    print("Connection Failed")

def handlePresenceChange(event):
    print("Status change for ", event['user'])


#create list of users
'''
if sc.rtm_connect():
    api_call = sc.api_call("users.list")
    users = api_call.get('members')
    for user in users:
        userList[user] = 0
        
        #print(user['name'] + ' - ID : ' + user.get('id'))
'''




#determin when a user joins and leaves a channel
#create a command to print list of users and time in channel