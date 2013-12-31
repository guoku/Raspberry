#!/bin/bash

find . -name '*.pyc' -exec rm -f {} \; # clean pyc 
#rsync -avz --delete --exclude='settings.py'   qinzhoukan/  guoku@119.167.225.32:/data/www/cupertino/
rsync -avz --delete --exclude='settings.py' raspberry/  guoku@119.167.225.32:/data/www/raspberry/
