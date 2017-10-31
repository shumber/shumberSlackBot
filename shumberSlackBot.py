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
        events = sc.rtm_read()
        #print(event)
        for event in events:
            if event['type'] == "presence_change":
                handlePresenceChange(event)
            if event['type'] == "message:":
                if event['text'] == "/userRPG"
                    handleMessage(event)
            time.sleep(1)
else:
    print("Connection Failed")

def handlePresenceChange(event):
    print("Status change for ", event['user'])
    if event['presence'] == 'active':
        userlist[event['user']]['active'] = time.time()
    if event['presence'] == 'away':
        userlist[event['user']]['away'] = time.time()
        userlist[event['user']]['total'] += (userlist[event['user']]['away'] - userlist[event['user']]['active'])

def handleMessage(event):
    for key, value in userList.items():
        print("user: ", key, "Total Time: " value['total'])



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