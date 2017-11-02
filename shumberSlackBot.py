from dotenv import load_dotenv
from IdleRPGBot import IdleRPGBot
import os

load_dotenv('keys.env')
slack_token = os.environ['SLACK_API_TOKEN']
dbFileName = "users.db"
activeChannelName = "#bot_playground"

bot = IdleRPGBot(slack_token, activeChannelName, dbFileName)
bot.main()
