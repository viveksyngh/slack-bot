
def pre_deployment(value):
	return "I will do that. Tell me which apllication you want to deploy.\
Backend or Frontend?"


def app_deployment(value):
	if value.upper() == 'BACKEND':
		# Call function to deploy backend code
		pass 
	elif value.upper() == 'FRONTEND':
		# Call function to deploy backend code
		pass
	return "I have started %s application deployment. \
I will notify you once it is done. Cheers!!!"%(value)

def greeting(value):
	return "Hello !! How can I help you ?"

RESPONSE_FUNC_MAP = {
	'pre_deploy' : pre_deployment,
	'application_name': app_deployment,
	'greeting' : greeting
}


