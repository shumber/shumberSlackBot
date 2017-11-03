import os
import time
from slackclient import SlackClient
import logging
import pickle
import copy

READ_EVENT_PAUSE = .1
class IdleRpgBot():
    def __init__(self, slack_token, active_channel_name, db_filename = "users.db"):
        self.slack_token = slack_token
        self.active_channel_name = active_channel_name
        self.sc = SlackClient(slack_token)
        self.userList = {}
        self.fb_filename = db_filename
        self.userListOld ={}
        self.load()

    def save(self):
        current_users = copy.deepcopy(self.userList)
        with open(self.fb_filename, 'wb') as db_file:
            pickle.dump(current_users, db_file, protocol=pickle.HIGHEST_PROTOCOL)
    
    def load(self):
        if os.path.isfile(self.fb_filename):
            with open(self.fb_filename, 'rb') as db_file:
                self.usersListOld = pickle.load(db_file)

    def handlePresenceChange(self, event, user): #Log the users score as they enter and leave the chat
        if event['presence'] == 'active':
            print("Status Active for ", event['user'], " - ", self.userList[event['user']]['total'])
            self.userList[event['user']]['active'] = time.time()
            self.userList[user['id']]['activeFlag'] = 1  
        if event['presence'] == 'away':
            print("Status Away for ", event['user'], " - ", self.userList[event['user']]['name'])
            self.userList[event['user']]['away'] = time.time()
            self.userList[user['id']]['activeFlag'] = 0
            self.userList[event['user']]['total'] = self.userListOld[user['id']]['total']+(self.userList[event['user']]['away'] - self.userList[event['user']]['active'])       

    def handlemessage(self, event):
        print(event)
        con="The Parties score for:"
        for key, value in self.userList.items():
            total= value['total']
            if value['isBot'] == 0:
                if value['activeFlag'] == 1:
                    level = time.time() - self.userList[event['user']]['active'] + self.userList[event['user']]['total'] + self.userListOld[user['id']]['total']
                    self.userList[event['user']]['total'] = level #the score at the time of the message 
                con +=("\n "+ value['name']+ " is " +str(int(level)))
        self.sc.api_call(
            "chat.postMessage", 
            channel="#bot_playground",
            text=con
            ) ##Sumting the score and message
        print(event['text'])  
        print("Message from", event['user'], " - ", self.userList[event['user']]['name'], event['text'])

    def MyLevel(self, event):
        level = time.time() - self.userList[event['user']]['active'] + self.userList[event['user']]['total'] + self.userListOld[user['id']]['total'] #the score at the time of the message 
        text=(self.userList[event['user']]['name']+ " your score is " +str(int(level)))
        self.userList[event['user']]['total'] = total
        self.sc.api_call(
                "chat.postMessage", 
                channel="#bot_playground",
                text=text
                )

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
                for event in events:
                    if event['type'] == "presence_change":
                        print("Activity")
                        self.handlePresenceChange(event, user)
                        self.save()
                    elif event['type'] == "message":
                        print("Message Recived")
                        if event['text'] == "TheScore":
                            self.handlemessage(event)
                            print("Message Sent")
                            self.save()
                        if event['text'] =="MyLevel":
                            self.MyLevel(event)
                            self.save()
                time.sleep(READ_EVENT_PAUSE)
                self.save()
        else:
            print("Connection Failed")
        
   