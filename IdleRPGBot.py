
from slackclient import SlackClient
from dotenv import load_dotenv
import os
import time
import pickle
import copy

class IdleRPGBot():
    def __init__(self, slack_token, activeChannelName, dbFileName):
        self.slack_token = slack_token
        self.activeChannelName = activeChannelName
        self.sc = SlackClient(slack_token)
        self.users = {}
        self.userList = {}
        self.fb_filename = dbFileName
        #self.load()

    def handlePresenceChange(self, event):
        if event['presence'] == 'active':
            print("Status Active for ", event['user'], " - ", self.userList[event['user']]['name'])
            self.userList[event['user']]['active'] = time.time()
            self.userList[event['user']]['activeFlag'] = True #Flag set when presence changes to active
        if event['presence'] == 'away':
            print("Status Away for ", event['user'], " - ", self.userList[event['user']]['name'])
            self.userList[event['user']]['away'] = time.time()
            self.userList[event['user']]['activeFlag'] = False #Flag reset when presence changes to away
            self.userList[event['user']]['total'] = self.userList[event['user']]['total'] + (self.userList[event['user']]['away'] - self.userList[event['user']]['active'])


    def RPGScore(self, event):
        text = "Hi, " + self.userList[event['user']]['name'] + "! The current RPG User scores are:"
        for key, value in self.userList.items():
            if value['isBot'] == False:
                if value['activeFlag'] == True: #if a user is active, we want to include their current active time in score without having to wait for a status change to away.
                    totalScore = time.time() - self.userList[event['user']]['active']
                else:
                    totalScore = value['total'] #if not active, we just used the stored total score.
                text += ("\n" + value['name'] + " - Score: " + str(int(totalScore)))            
        channel = "#bot_playground"
        self.printMessageToChannel(text, channel)

    def botHelp(self, event):
        text = "Hi, " + self.userList[event['user']]['name'] + "! I can help you with the following commands:"
        text += "\n   RPGScore"
        text += "\n   help"
        channel = "#bot_playground"
        self.printMessageToChannel(text, channel)

    def printMessageToChannel(self, text, channel):
        self.sc.api_call(
            "chat.postMessage",
            channel=channel,
            #channel="#bot_playground",
            text=text
            )

    def main(self):
        if self.sc.rtm_connect(): #connect to slack 
            api_call = self.sc.api_call("users.list", presence="true")
            users = api_call.get('members')
            for user in users:
                self.userList[user['id']] = {}
                self.userList[user['id']]['active'] = 0.0 #Active timestamp
                self.userList[user['id']]['away'] = 0.0  #Away timestamp
                self.userList[user['id']]['total'] = 0.0 #Total time Idle
                self.userList[user['id']]['name'] = user['profile']['real_name']
                self.userList[user['id']]['activeFlag'] = False #indicates if user is currently active
                self.userList[user['id']]['isBot'] = True #bot flag - True is bot, False is not
                if user['id'] != "USLACKBOT":
                    if user['deleted'] == False: #Ignore deleted users
                        if user['is_bot'] == False: #Ignore bots
                            self.userList[user['id']]['isBot'] = False #any users at this point are not bots
                            if user['presence'] == "active": #if user is active, we want to set their active time without having to wait for a presence change.
                                self.userList[user['id']]['active'] = time.time()
                                self.userList[user['id']]['activeFlag'] = True 

            #print(userList)    
            while True:
                events = self.sc.rtm_read()
                print(events)
                for event in events:
                    if event['type'] == "presence_change":
                        self.handlePresenceChange(event)
                    elif event['type'] == "message":
                        if "<@U7SD52QJV>" in event['text']:
                            if event['text'] == "<@U7SD52QJV> RPGScore":
                                self.RPGScore(event)
                            elif "?" in event['text']:
                                self.botHelp(event)
                            elif "help" in event['text']:
                                self.botHelp(event)
                time.sleep(1)
        else:
            print("Connection Failed")

    if __name__ == '__main__':
        main()


    #Make classes
    #Seperate into files
    #Add logging statements
    #Make sure to set all users as offline, and stamp their end times.