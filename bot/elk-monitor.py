import requests
import json
from config import SLACK_BOT_TOKEN
from slackclient import SlackClient
ELASTIC_URL = "http://localhost:81/_count"
#CHANNEL = "D2CDFTA7M"
CHANNEL = "C38H6U9L0"
from time import sleep
data = { 
	"query": { 
		"range" : { 
			"@timestamp": { 
				"gte": "now-15m"
				} 
			} 
		} 
	}

def get_last_15_min_documents():
	try:
		res = requests.get(ELASTIC_URL, data=json.dumps(data))
		response_data = json.loads(res.text)
	except Exception, e:
		send_error_message()
	else:
		if response_data["count"] == 0:
			send_null_message()
		else:
			send_success_message(response_data["count"])


def send_error_message():
	slack_client = SlackClient(SLACK_BOT_TOKEN)
	message = "There is someting wrong with server, Either log server is down or \
elasticsearch server is down. Please login to server to fix the issue asap."
	channel = CHANNEL
        slack_client.api_call("chat.postMessage", channel=channel, text=message, as_user=True)
		

def send_success_message(count):
	slack_client = SlackClient(SLACK_BOT_TOKEN)
	message = "Log server is doing great. It hase created {0} documents in last 15 min. Have a great day!!".format(count)
	channel = CHANNEL
        slack_client.api_call("chat.postMessage", channel=channel, text=message, as_user=True)
			
def send_null_message():
	slack_client = SlackClient(SLACK_BOT_TOKEN)
	message = "Elastic search is running but It seems it has not received any logs is last 15 min.Try restarting logstash service."
	channel = CHANNEL
        slack_client.api_call("chat.postMessage", channel=channel, text=message, as_user=True)

while True:
	get_last_15_min_documents()
	sleep(900)
