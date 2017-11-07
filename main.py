from IdleRpgBot.IdleRpgBot import IdleRpgBot
import os
import logging
from dotenv import load_dotenv

def main():
    logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)
    load_dotenv('.env')
    slack_token = os.environ["SLACK_API_TOKEN"]
    active_channel_name="#bot_playground"
    sc = IdleRpgBot(slack_token, active_channel_name)
    userList = {}
    sc.connect()

if __name__ == '__main__':
    main()