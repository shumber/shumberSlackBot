
from slackclient import SlackClient
from dotenv import load_dotenv
import os
import time
import pickle
import copy

load_dotenv('keys.env')

slack_token = os.environ['SLACK_API_TOKEN']
sc = SlackClient(slack_token)
userList = {}

class idleRPGBot():
    def __init__(self, slack_token, activeChannelName, dbFileName):
    self.slack_token = slack_token
    self.activeChannelName = active_channel_name
    self.sc = SlackClient(slack_token)
    self.users = {}
    self.fb_filename = db_filename
    self.load()

    def handlePresenceChange(self, event):
        if event['presence'] == 'active':
            print("Status Active for ", event['user'], " - ", userList[event['user']]['name'])
            userList[event['user']]['active'] = time.time()
            userList[event['user']]['activeFlag'] = True #Flag set when presence changes to active
        if event['presence'] == 'away':
            print("Status Away for ", event['user'], " - ", userList[event['user']]['name'])
            userList[event['user']]['away'] = time.time()
            userList[event['user']]['activeFlag'] = False #Flag reset when presence changes to away
            userList[event['user']]['total'] = userList[event['user']]['total'] + (userList[event['user']]['away'] - userList[event['user']]['active'])


    def RPGScore(self, event):
        text = "Hi, " + userList[event['user']]['name'] + "! The current RPG User scores are:"
        for key, value in userList.items():
            if value['isBot'] == False:
                if value['activeFlag'] == True: #if a user is active, we want to include their current active time in score without having to wait for a status change to away.
                    totalScore = time.time() - userList[event['user']]['active']
                else:
                    totalScore = value['total'] #if not active, we just used the stored total score.
                text += ("\n" + value['name'] + " - Score: " + str(int(totalScore)))            
        channel = "#bot_playground"
        printMessageToChannel(text, channel)

    def botHelp(self, event):
        text = "Hi, " + userList[event['user']]['name'] + "! I can help you with the following commands:"
        text += "\n   RPGScore"
        text += "\n   help"
        channel = "#bot_playground"
        printMessageToChannel(text, channel)

    def printMessageToChannel(self, text, channel):
        sc.api_call(
            "chat.postMessage",
            channel=channel,
            #channel="#bot_playground",
            text=text
            )

    def main(self):
        if sc.rtm_connect(): #connect to slack 
            api_call = sc.api_call("users.list", presence="true")
            users = api_call.get('members')
            for user in users:
                userList[user['id']] = {}
                userList[user['id']]['active'] = 0.0 #Active timestamp
                userList[user['id']]['away'] = 0.0  #Away timestamp
                userList[user['id']]['total'] = 0.0 #Total time Idle
                userList[user['id']]['name'] = user['real_name']
                userList[user['id']]['activeFlag'] = False #indicates if user is currently active
                userList[user['id']]['isBot'] = True #bot flag - True is bot, False is not
                if user['id'] != "USLACKBOT":
                    if user['deleted'] == False: #Ignore deleted users
                        if user['is_bot'] == False: #Ignore bots
                            userList[user['id']]['isBot'] = False #any users at this point are not bots
                            if user['presence'] == "active": #if user is active, we want to set their active time without having to wait for a presence change.
                                userList[user['id']]['active'] = time.time()
                                userList[user['id']]['activeFlag'] = True 

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
                                RPGScore(event)
                            elif "?" in event['text']:
                                botHelp(event)
                            elif "help" in event['text']:
                                botHelp(event)
                time.sleep(1)
        else:
            print("Connection Failed")

    if __name__ == '__main__':
        main()


    #Make classes
    #Seperate into files
    #Add logging statements
    #Make sure to set all users as offline, and stamp their end times.