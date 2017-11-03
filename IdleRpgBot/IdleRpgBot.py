import os
import time
from slackclient import SlackClient
import logging
import pickle
import copy

class IdleRpgBot():
    def __init__(self, slack_token, active_channel_name, db_filename = "users.db"):
        self.slack_token = slack_token
        self.active_channel_name = active_channel_name
        self.sc = SlackClient(slack_token)
        self.userList = {}

    def save(self):
        current_users = copy.deepcopy(self.users)
        with open(self.fb_filename, 'wb') as db_file:
            pickle.dump(current_users, db_file, protocol=pickle.HIGHEST_PROTOCOL)
    
    def load(self):
        if os.path.isfile(self.fb_filename):
            with open(self.fb_filename, 'rb') as db_file:
                self._users = pickle.load(db_file)

    def handlePresenceChange(self, event, user): #Log the users score as they enter and leave the chat
        if event['presence'] == 'active':
            print("Status Active for ", event['user'], " - ", self.userList[event['user']]['name'])
            self.userList[event['user']]['active'] = time.time()
            self.userList[user['id']]['activeFlag'] = 1
        if event['presence'] == 'away':
            print("Status Away for ", event['user'], " - ", self.userList[event['user']]['name'])
            self.userList[event['user']]['away'] = time.time()
            self.userList[user['id']]['activeFlag'] = 0
            self.userList[event['user']]['total'] = self.userList[event['user']]['total'] + (self.userList[event['user']]['away'] - self.userList[event['user']]['active'])
        self.load()
       

    def handlemessage(self, event):
        print(event)
        con="The Parties score for:"
        for key, value in self.userList.items():
            if value['isBot'] == 0:
                if value['activeFlag'] == 1:
                    level = time.time() - self.userList[event['user']]['active'] + self.userList[event['user']]['total'] #the score at the time of the message 
                else: 
                    level = value['total']
                con +=("\n "+ value['name']+ " is " +str(int(level)))
        self.sc.api_call(
            "chat.postMessage", 
            channel="#bot_playground",
            text=con
            ) ##Sumting the score and message
        print(event['text'])  
        print("Message from", event['user'], " - ", self.userList[event['user']]['name'], event['text'])
    self.load()

    def MyLevel(self, event):
        level = time.time() - self.userList[event['user']]['active'] + self.userList[event['user']]['total'] #the score at the time of the message 
        text=(self.userList[event['user']]['name']+ " your score is " +str(int(level)))
        self.sc.api_call(
                "chat.postMessage", 
                channel="#bot_playground",
                text=text
                )
    self.load()

    def connect(self):
        if self.sc.rtm_connect(): #connect to slack 
            api_call = self.sc.api_call("users.list", presence="true")
            users = api_call.get('members')
            ##greeting="Here we go" ##Nice to meet you. Type Score to see your RPG total
            ##sc.api_call("chat.postMessage", channel="#bot_playground", text=greeting, )
            for user in users:
                self.userList[user['id']] = {}
                self.userList[user['id']]['active'] = 0.0
                self.userList[user['id']]['away'] = 0.0
                self.userList[user['id']]['total'] = 0.0
                self.userList[user['id']]['name'] = user['profile']['real_name']
                self.userList[user['id']]['activeFlag'] = 0
                self.userList[user['id']]['isBot'] = 1
                if user['id'] != "USLACKBOT":
                    if user['deleted'] == False:
                        if user['is_bot']==False:
                            self.userList[user['id']]['isBot']= 0
                            if user['presence']=="active":
                                self.userList[user['id']]['active'] = time.time()
                                self.userList[user['id']]['activeFlag'] = 1  
            while True:
                events = self.sc.rtm_read()
                print(events)
                for event in events:
                    if event['type'] == "presence_change":
                        print("Activity")
                        self.handlePresenceChange(event, user)
                    elif event['type'] == "message":
                        print("Message Recived")
                        if event['text'] == "TheScore":
                            self.handlemessage(event)
                            print("Message Sent")
                        if event['text'] =="MyLevel":
                            self.MyLevel(event)
                time.sleep(1)
        else:
            print("Connection Failed")
    self.load()