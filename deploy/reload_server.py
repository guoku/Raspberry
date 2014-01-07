#!/usr/bin/env python


from fabric.api import *
from fabric.context_managers import *


env.hosts=['114.113.154.47' ]
env.user='jiaxin'

def reload_gunicorn():
	with cd('/opt/script/'):
		sudo('/bin/bash ./gunicorn reload')

# def reload_gunicorn():
# 	# with cd(''):
# 	run('sh gunicorn reload')


def reload():
	# execute(sudo)
	execute(reload_gunicorn)
