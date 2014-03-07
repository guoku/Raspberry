#!/usr/bin/env python


import ConfigParser
import os

from fabric.api import *
from fabric.context_managers import *
from fabric.contrib.project import rsync_project

Config = ConfigParser.ConfigParser()
Config.read('config.ini')

root_dir = os.path.join(os.getcwd(), '..')

env.hosts = ['114.113.154.46' ]

env.user = Config.get('global', 'user')
env.key = os.path.join(root_dir, Config.get('global', 'key'))


# Where the static files get collected locally. Your STATIC_ROOT setting.
env.local_static_root = '/tmp/static/'

# Where the static files should go remotely
env.remote_static_root = '/data/www/core/static/v3/'

def deploy_static():
    with lcd('/Users/edison7500/PycharmProjects/Raspberry/raspberry'):
        local('python manage.py collectstatic --noinput --settings="raspberry.settings.production"')
    rsync_project(
        remote_dir = env.remote_static_root,
        local_dir = env.local_static_root,
#        delete = True
    )
