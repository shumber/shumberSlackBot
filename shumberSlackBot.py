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
        userList[user['id']]['activeFlag'] = 1
    if event['presence'] == 'away':
        print("Status Away for ", event['user'], " - ", userList[event['user']]['name'])
        userList[event['user']]['away'] = time.time()
        userList[user['id']]['activeFlag'] = 0
        userList[event['user']]['total'] = userList[event['user']]['total'] + (userList[event['user']]['away'] - userList[event['user']]['active'])
       

def handlemessage(event):
    print("Message from", event['user'], " - ", userList[event['user']]['name'])
    for key, value in userList.items():
        if value['isBot'] == 1:
            if value['activeFlag'] == 1:
                level = time.time() - userList[event['user']]['active'] + value['total']  #the score at the time of the message 
            else: 
                level = value['total']
            con =( "The Parties score for: " + "\n "+ value['name']+ "is" +str(int(level)))
    sc.api_call('chat.postMessages', channel="#bot_playground", text=con) ##Sumiting the score and message


if sc.rtm_connect(): #connect to slack 
    api_call = sc.api_call("users.list", presence="true")
    users = api_call.get('members')
    ##greeting="Here we go" ##Nice to meet you. Type Score to see your RPG total
    ##sc.api_call("chat.postMessage", channel="#bot_playground", text=greeting, )
    for user in users:
        userList[user['id']] = {}
        userList[user['id']]['active'] = 0.0
        userList[user['id']]['away'] = 0.0
        userList[user['id']]['total'] = 0.0
        userList[user['id']]['name'] = user['name']
        userList[user['id']]['activeFlag'] = 0
        userList[user['id']]['isBot'] = 0
        if user['id'] != "USLACKBOT":
            if user['deleted'] == False:
                if user['is_bot']==False:
                    userList[user['id']]['isBot']= 1
                    if user['presence']=="active":
                        userList[user['id']]['active'] = time.time()
                        userList[user['id']]['activeFlag'] = 1
    
    while True:
        events = sc.rtm_read()
        print(events)
        for event in events:
            if event['type'] == "presence_change":
                print("Activity")
                handlePresenceChange(event)
            if event["type"] == "message" and event['text'] == "Post":
                    print("Message Recived")
                    handlemessage(event)
        time.sleep(1)
else:
    print("Connection Failed")
