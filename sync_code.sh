#!/bin/bash

find . -name '*.pyc' -exec rm -f {} \; # clean pyc 
rsync -avz --delete raspberry/  jiaxin@114.113.154.46:/data/www/raspberry/
rsync -avz --delete raspberry/base/static/css/ jiaxin@114.113.154.46:/data/www/core/static/v3/css/
#rsync -avz --exclude='settings.py'  raspberry/  jiaxin@10.0.2.218:/data/www/raspberry/
#rsync -avz --exclude='settings.py'  raspberry/  stxiong@10.0.2.217:/data/www/raspberry/
