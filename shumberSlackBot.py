import os
import time
from slackclient import SlackClient
from dotenv import load_dotenv

load_dotenv('keys.env')

slack_token = os.environ['SLACK_API_TOKEN']
sc = SlackClient(slack_token)
userList = {}

def handlePresenceChange(event):
    if event['presence'] == 'active':
        print("Status Active for ", event['user'], " - ", userList[event['user']]['name'])
        userList[event['user']]['active'] = time.time()
        userList[event['user']]['activeFlag'] = 1 #Flag set when presence changes to active
    if event['presence'] == 'away':
        print("Status Away for ", event['user'], " - ", userList[event['user']]['name'])
        userList[event['user']]['away'] = time.time()
        userList[event['user']]['activeFlag'] = 0 #Flag reset when presence changes to away
        userList[event['user']]['total'] = userList[event['user']]['total'] + (userList[event['user']]['away'] - userList[event['user']]['active'])


def handleMessage(event):
    text = "Hi, " + userList[event['user']]['name'] + "! The current RPG User scores are:"
    for key, value in userList.items():
        if value['isBot'] == 0:
            if value['activeFlag'] == 1: #if a user is active, we want to include their current active time in score without having to wait for a status change to away.
                totalScore = time.time() - userList[event['user']]['active']
            else:
                totalScore = value['total'] #if not active, we just used the stored total score.
            text += ("\n" + value['name'] + " - Score: " + str(int(totalScore)))            
    sc.api_call(
        "chat.postMessage",
        channel="#bot_playground",
        text=text
        )

def botHelp(event):
    text = "Hi, " + userList[event['user']]['name'] + "! I can help you with the following commands:"
    text += "\n   RPGScore"
    text += "\n   help"
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
        userList[user['id']]['name'] = user['real_name']
        userList[user['id']]['activeFlag'] = 0 #indicates if user is currently active
        userList[user['id']]['isBot'] = 1 #bot flag
        if user['id'] != "USLACKBOT":
            if user['deleted'] == False: #Ignore deleted users
                if user['is_bot'] == False: #Ignore bots
                    userList[user['id']]['isBot'] = 0 #any users at this point are not bots
                    if user['presence'] == "active": #if user is active, we want to set their active time without having to wait for a presence change.
                        userList[user['id']]['active'] = time.time()
                        userList[user['id']]['activeFlag'] = 1 

    #print(userList)    
    while True:
        events = sc.rtm_read()
        print(events)
        for event in events:
            if event['type'] == "presence_change":
                handlePresenceChange(event)
            elif event['type'] == "message":
                if "<@U7SD52QJV>" in event['text']:
                    if event['text'] == "<@U7SD52QJV> RPGScore":
                        handleMessage(event)
                    elif "?" in event['text']:
                        botHelp(event)
                    elif "help" in event['text']:
                        botHelp(event)
        time.sleep(1)
else:
    print("Connection Failed")
