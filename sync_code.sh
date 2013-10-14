#!/bin/bash

find . -name '*.pyc' -exec rm -f {} \; # clean pyc 
rsync -avz --exclude='settings.py'  raspberry/  jiaxin@10.0.2.217:/data/www/raspberry/
rsync -avz --exclude='settings.py'  raspberry/  jiaxin@10.0.2.218:/data/www/raspberry/
#rsync -avz   raspberry/  jiaxin@10.0.2.217:/data/www/raspberry/
#rsync -avz   raspberry/  jiaxin@10.0.2.218:/data/www/raspberry/
