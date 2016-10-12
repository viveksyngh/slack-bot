from fabfile import kuch_kar
import os
from slackclient import SlackClient
from config import SLACK_BOT_TOKEN

def pre_deployment(value, channel):
	return "I will do that. Tell me which apllication you want to deploy.\
Backend or Frontend?"


def app_deployment(value, channel):
	if value.upper() == 'BACKEND':
		# Call function to deploy backend code
		try:
			os.system('fab kuch_kar:devops_deployment,8004')
		except:
			slack_client = SlackClient(SLACK_BOT_TOKEN)
			slack_client.api_call("chat.postMessage", channel=channel,
							  text="Falied deployment", as_user=True)
	elif value.upper() == 'FRONTEND':
		# Call function to deploy backend code
		pass
	return "I have started %s application deployment. \
I will notify you once it is done. Cheers!!!"%(value)

def greeting(value, channel):
	return "Hello !! How can I help you ?"

RESPONSE_FUNC_MAP = {
	'pre_deploy' : pre_deployment,
	'application_name': app_deployment,
	'greeting' : greeting
}


