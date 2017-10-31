import os
from slackclient import SlackClient

slack_token = os.environ['SLACK_API_TOKEN']
sc = SlackClient(slack_token)

sc.api_call(
  "chat.postMessage",
  channel="#general",
  text="Hello from scottSlackBot! :tada:"
)