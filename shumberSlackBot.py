import os
import time
from slackclient import SlackClient
from dotenv import load_dotenv


load_dotenv('.env')
slack_token = os.environ["SLACK_API_TOKEN"]
sc = SlackClient(slack_token)
userList = {}

def handlePresenceChange(event): #Log the users score as they enter and leave the chat
   if event['presence'] == 'active':
        print("Status Active for ", event['user'], " - ", userList[event['user']]['name'])
        userList[event['user']]['active'] = time.time()
        userList[event['user']]['activeFlag'] = 1 #Flag set when presence changes to active
   if event['presence'] == 'away':
        print("Status Away for ", event['user'], " - ", userList[event['user']]['name'])
        userList[event['user']]['away'] = time.time()
        userList[event['user']]['activeFlag'] = 0 #Flag reset when presence changes to away
        userList[event['user']]['total'] = userList[event['user']]['total'] + (userList[event['user']]['away'] - userList[event['user']]['active'])


def handle_message(event):
    text = "RPG User scores:"
    for key, value in userList.items():
        if value['isBot'] == 0:
            if value['activeFlag'] == 1: #if a user is active, we want to include their current active time in score without having to wait for a status change to away.
                totalScore = time.time() - userList[event['user']]['active']
            else:
                totalScore = value['total'] #if not active, we just used the stored total score.
            text += ("\nuser:" + value['name'] + " - Score: " + str(int(totalScore)))            
    sc.api_call(
        "chat.postMessage",
        channel="#bot_playground",
        text=text
        )


if sc.rtm_connect(): #connect to slack 
  api_call = sc.api_call("users.list", presence="true")
    users = api_call.get('members')
    for user in users:
        userList[user['id']] = {}
        userList[user['id']]['active'] = 0.0
        userList[user['id']]['away'] = 0.0
        userList[user['id']]['total'] = 0.0
        userList[user['id']]['name'] = user['name']
        userList[user['id']]['activeFlag'] = 0 #indicates if user is currently active
        userList[user['id']]['isBot'] = 1 #bot flag
        if user['id'] != "USLACKBOT":
            if user['deleted'] == False: #Ignore deleted users
                if user['is_bot'] == False: #Ignore bots
                    userList[user['id']]['isBot'] = 0 #any users at this point are not bots
                    if user['presence'] == "active": #if user is active, we want to set their active time without having to wait for a presence change.
                        userList[user['id']]['active'] = time.time()
                        userList[user['id']]['activeFlag'] = 1 

    while True:
        events = sc.rtm_read()
        print(events)
        for event in events:
            if event['type'] == "presence_change":
                handlePresenceChange(event)
            elif event['type'] == "message":
                if event['text'] == "Post":
                    handle_message(event)
        time.sleep(1)
else:
    print("Connection Failed")
