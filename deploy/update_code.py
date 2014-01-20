#!/usr/bin/env python


import ConfigParser
import os

from fabric.api import *
from fabric.context_managers import *
from fabric.contrib.project import rsync_project

Config = ConfigParser.ConfigParser()
Config.read('config.ini')

root_dir = os.path.join(os.getcwd(), '..')

env.hosts = ['114.113.154.47' ]

env.user = Config.get('global', 'user')
#env.key = Config.get('global', 'key')
env.key = os.path.join(root_dir, Config.get('global', 'key')) 

#env.local_root = Config.get('local', 'project_dir')
env.local_root = os.path.join(root_dir, Config.get('local', 'project_dir'))
env.project_root = Config.get('server', 'project_dir')

# print env.local_root

def update_code():
    local('git pull origin master')


def upload_code():
 	rsync_project(
 			remote_dir = env.project_root,
 			local_dir = env.local_root,
 			exclude = 'settings.py'
 		)

def upload():
#	execute(update_code)
	execute(upload_code)
