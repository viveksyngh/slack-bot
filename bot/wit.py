import os
import requests
import json
from slack_response import RESPONSE_FUNC_MAP
from config import WIT_TOKEN

#TOKEN = os.environ.get('WIT_TOKEN')
TOKEN = WIT_TOKEN
MESSAGE_URL = "https://api.wit.ai/message"
CONVERSE_URL = "https://api.wit.ai/converse"

def make_requests(message):
	payload = {
			"v" : "20141022",
			"q" : message[:256],
			"session_id" : '123abc'
		}
	headers = { "Authorization": "Bearer " + TOKEN}
	res = requests.post(CONVERSE_URL, params=payload, headers=headers)
	print res.text
	return res


def parse_wit_response(res):
	response_text = ''
	try:
		response = json.loads(res.text)
		entities = response["entities"]
		if len(entities) == 1:
			entity = entities.keys()[0]
			tags = entities[entity]
			tags.sort(key=lambda x : x['confidence'], reverse=True)
			tag = tags[0]
			func = RESPONSE_FUNC_MAP.get(entity)
			if func :
				response_text = func(tag["value"])
	except Exception :
		pass
	return response_text


def parse_converse_response(res):
	response_text = ''
	try:
		response = json.loads(res.text)
		if "type" in response:
			if response["type"] == "msg":
				response_text = response["msg"]
			elif response["type"] == "stop":
				response_text = ''
	except Exception:
		pass
	return response_text
