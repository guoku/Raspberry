#!/bin/bash

find . -name '*.pyc' -exec rm -f {} \; # clean pyc 
rsync -avz --exclude='settings.py'  raspberry/  jiaxin@114.113.154.47:/data/www/raspberry/
#rsync -avz --exclude='settings.py'  raspberry/  jiaxin@10.0.2.218:/data/www/raspberry/
#rsync -avz --exclude='settings.py'  raspberry/  stxiong@10.0.2.217:/data/www/raspberry/
<<<<<<< HEAD
=======
rsync -avz --exclude='settings.py'  raspberry/  jiaxin@114.113.154.47:/data/www/raspberry/
#rsync -avz   raspberry/  jiaxin@10.0.2.217:/data/www/raspberry/
#rsync -avz   raspberry/  jiaxin@10.0.2.218:/data/www/raspberry/
>>>>>>> 72c98056fc033cda5af285852a40fecffeb4980d
