#!/bin/bash

find . -name '*.pyc' -exec rm -f {} \; # clean pyc 
#rsync -avz --delete --exclude='settings.py'   qinzhoukan/  guoku@119.167.225.32:/data/www/cupertino/
rsync -avz --delete raspberry/  jiaxin@114.113.154.49:/data/www/raspberry/
