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
ver = local("git log | head -n 1 | awk '{print $2}'", capture=True)
print ver
static_path =  '/data/www/core/static/v3/%s/' % ver
env.remote_static_root = static_path

# local("sed -i 's/v3\/.*/v3\/%s/' settings/static.py" % ver)




def deploy_static():
    
    with lcd('/Users/edison/PycharmProjects/Raspberry/raspberry'):
        local('python manage.py collectstatic --noinput --settings="raspberry.settings.stage"')
        local('sh ../deploy/clean_static.sh')
        local('sed  "s/v3\/.*/v3\/%s\/\'/" settings/static.py > settings/static.py.tmp' % ver)
        local("mv settings/static.py.tmp settings/static.py")
    rsync_project(
        remote_dir = env.remote_static_root,
        local_dir = env.local_static_root,
#        delete = True
    )
    local('rm -rf /tmp/static/')
