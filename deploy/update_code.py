#!/usr/bin/env python


import ConfigParser

from fabric.api import *
from fabric.context_managers import *

Config = ConfigParser.ConfigParser()
Config.read('config.ini')


#env.user = Config.get('global', 'user')



def update_code():
    local('git pull origin master')
