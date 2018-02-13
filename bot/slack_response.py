from fabfile import kuch_kar
import os
from slackclient import SlackClient
from config import SLACK_BOT_TOKEN
import subprocess

def pre_deployment(value, channel):
	return "I will do that. Tell me which apllication you want to deploy.\
Backend or Frontend?"


def app_deployment(value, channel):
	slack_client = SlackClient(SLACK_BOT_TOKEN)
	if value.upper() == 'BACKEND':
		# Call function to deploy backend code
		try:
			# os.system('fab kuch_kar:devops_deployment,8004')
			slack_client.api_call("chat.postMessage", channel=channel,
							  text="I have started %s application deployment. \
I will notify you once it is done. Cheers!!!"%(value), as_user=True)
			p = subprocess.Popen(["fab", "kuch_kar:'devops_deployment',8006"])
			a, b = p.communicate()
		except Exception, e:
			return "Failed to deploy application. Try once again!!"
	elif value.upper() == 'FRONTEND':
		# Call function to deploy backend code
		pass
	if p.returncode:
		# slack_client.api_call("chat.postMessage", channel=channel,
		# 					  text="Deployment was unsuccessful.", as_user=True)
		return "Deployment was unsuccessful."
		# slack_client.api_call("chat.postMessage", channel=channel,
		# 					  text="Deployment was successful.", as_user=True)
	return "Deployment was successful. Here is url to your application. http://localhost:8006/"

def greeting(value, channel):
	return "Hello !! How can I help you ?"

RESPONSE_FUNC_MAP = {
	'pre_deploy' : pre_deployment,
	'application_name': app_deployment,
	'greeting' : greeting
}


