#!/usr/bin/env python


from fabric.api import *
from fabric.context_managers import *


env.hosts=['114.113.154.46', '114.113.154.48']
env.user='jiaxin'
env.password='jessie1@#'

def reload_gunicorn():
	with cd('/opt/script/'):
		run('sudo /bin/bash ./gunicorn reload')

# def reload_gunicorn():
# 	# with cd(''):
# 	run('sh gunicorn reload')


def reload():
	# execute(sudo)
	execute(reload_gunicorn)