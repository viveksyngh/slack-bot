from __future__ import with_statement
from fabric.api import local, env, settings, abort, run, cd
from fabric.contrib.console import confirm
import time
import random

env.use_ssh_config = False
env.hosts = ['localhost']
CELERY = 'celery'
# env.hosts = ['104.236.85.162']
env.user = 'vivek'
env.key_filename = '~/.ssh/id_rsa.pub'

staging_branch = 'STAGING'
testing_branch = 'TESTING'
development_branch = 'DEVELOPMENT'
#team1_branch = 'PROD1'
#team2_branch = 'PROD2'
#team3_branch = 'PROD3'
#team4_branch = 'PROD4'
checkout_directory = '/happay_v2'

branch_list = [staging_branch,
	       testing_branch,
                development_branch]
               #, team1_branch,
		#		team2_branch, team3_branch, team4_branch]

base_dir = '/home/vivek/learning/slackbot'
base_repo_dir = base_dir + '/repos'
code_staging_dir=base_repo_dir + '/staging'
code_testing_dir=base_repo_dir + '/testing'
code_development_dir=base_repo_dir + '/development'

branch_map = {
	code_staging_dir : staging_branch,
	code_testing_dir : testing_branch,
	code_development_dir : development_branch
}

port_map = {
	staging_branch : '8081',
	testing_branch : '8082',
	development_branch : '8083'
}

def kuch_kar(branch, port):
	if branch not in branch_list:
		dir_path = base_repo_dir + '/' + branch.lower()
		make_dir(dir_path)
		clone_repo(dir_path, branch)
		kar_docker_build(dir_path, branch, port)
	else:
		dir_path = base_repo_dir + '/' + branch.lower()
		kar_docker_build(dir_path, branch)

def kar_path_create():
	for branch in branch_list:
		dir_path = base_repo_dir + '/' + branch.lower()
		make_dir(dir_path)

def kar_clone():
	for branch in branch_list:
		dir_path = base_repo_dir + '/' + branch.lower()
		clone_repo(dir_path, branch)

def kar_build():
	print(branch_list)
	for branch in branch_list:
		dir_path = base_repo_dir + '/' + branch.lower()
		kar_docker_build(dir_path, branch)

def kar_docker_build(path, branch, basic_port = None):
	with cd(path+checkout_directory):
		checkout_branch = branch
		run("git checkout %s"%(checkout_branch))
		run("git pull origin %s"%(checkout_branch))
		run("docker build -t %s ."%(checkout_branch.lower()))
		run("docker tag %s happay/%s"%(checkout_branch.lower(), checkout_branch.lower()))
		if basic_port:
			port = basic_port
		else:
			port = port_map.get(checkout_branch)
			if not port:
				port = random.randrange(8100,8200)

		# run("docker run -p %s:8000 %s"%(port, checkout_branch.lower()))
		print path+checkout_directory
		run("docker run --env-file env.list -d -p %s:8000 %s"%(port, checkout_branch.lower()))

def make_dir(path):
	with cd(base_dir):
		with settings(warn_only=True):
			run("mkdir -p %s"%(path))


def clone_repo(path, branch):
	with cd(path):
		with settings(warn_only=True):
			run("git clone ssh://git@bitbucket.org/CavacServ9/happay_v2.git")
			run("git fetch && git checkout %s"%(branch))


# def kar_path_create():
# 	make_dir(code_staging_dir)
# 	make_dir(code_testing_dir)
# 	make_dir(code_development_dir)

# def kar_clone():
# 	clone_repo(code_staging_dir)
# 	clone_repo(code_testing_dir)
# 	clone_repo(code_development_dir)

# def kar_build():
# 	kar_docker_build(code_staging_dir)
# 	kar_docker_build(code_testing_dir)
# 	kar_docker_build(code_development_dir)

# def kar_docker_build(path):
# 	with cd(path+checkout_directory):
# 		checkout_branch = branch_map[path]
# 		run("git fetch && git checkout %s"%(checkout_branch))
# 		run("git pull origin %s"%(checkout_branch))
# 		run("docker build -t %s ."%(checkout_branch.lower()))
# 		run("docker tag %s happay/%s"%(checkout_branch.lower(), checkout_branch.lower()))
# 		port = port_map[checkout_branch]
# 		run("docker run -p %s:8000 %s"%(port, checkout_branch.lower()))

# def make_dir(path):
# 	with cd(base_dir):
# 		with settings(warn_only=True):
# 			run("mkdir -p %s"%(path))


# def clone_repo(path):
# 	with cd(path):
# 		with settings(warn_only=True):
# 			run("git clone https://arriqaaq321@bitbucket.org/CavacServ9/happay_v2.git")


