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

def handlePresenceChange(event):
    print("Status change for ", event['user'])
    if event['presence'] == 'active':
        userList[event['user']]['active'] = time.time()
    if event['presence'] == 'away':
        userList[event['user']]['away'] = time.time()
        userList[event['user']]['total'] += (userList[event['user']]['away'] - userList[event['user']]['active'])
        print(userList[event['user']]['total'])

def handle_message(event):
    for key, value in userList.items():
       print('user: ', key, "Total Time", value['total'])


if sc.rtm_connect(): #connect to slack 
    api_call = sc.api_call("users.list")
    users = api_call.get('members')
    chan="#bot_playground"
    greeting="Hello!" ##Nice to meet you. Type Score to see your RPG total
    sc.api_call("chat.postMessage", channel=chan, text=greeting)
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
                if event['text'] == "Score":
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