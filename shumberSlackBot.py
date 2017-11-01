import os
import time
from slackclient import SlackClient
from dotenv import load_dotenv


load_dotenv('.env')
slack_token = os.environ["SLACK_API_TOKEN"]
sc = SlackClient(slack_token)
userList = {}
'''
sc.api_call(
  "chat.postMessage",
  channel="#bot_playground",
  text="Hello from scottSlackBot! :tada:"
)
'''

def handle_Presence_Change(event):
    print("Status change for ", event['user'])
    if event['presence']=="active":
        user.event[event['user']]['active']=time.time()
    if event['presence']=="away":
        user.event[event['user']]['away']=time.time()
        user.event[event['user']]['total'] += user.event[event['user']]['away'] - user.event[event['user']]['active']
        print(userList[event['user']]['total'])

def handle_message(event):
    for key, value in userList.items():
        print('user'+"Total Time" + value['total'])


if sc.rtm_connect(): #connect to slack 
    api_call = sc.api_call("users.list")
    users = api_call.get('members')
    for user in users:
        userList[user['id']] = {}
        userList[user['id']]['active'] = 0
        userList[user['id']]['away'] = 0
        userList[user['id']]['total'] = 0
    while True:
        events = sc.rtm_read()
        print(events)
        for event in events:
            if event['type'] == "presence_change":
                handlePresenceChange(event)
            if event['type'] == "message:":
                if event['text'] == "/userRPG":
                    handleMessage(event)
            time.sleep(1)
else:
    print("Connection Failed")

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
#create a command to print list of users and time in 