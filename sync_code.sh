#!/bin/bash

find . -name '*.pyc' -exec rm -f {} \; # clean pyc 
rsync -avz --delete raspberry/  jiaxin@114.113.154.46:/data/www/raspberry/
rsync -avz --delete raspberry/base/static/css/ jiaxin@114.113.154.46:/data/www/core/static/v3/css/
rsync -avz --delete raspberry/base/static/js/ jiaxin@114.113.154.46:/data/www/core/static/v3/js/
rsync -avz --delete raspberry/base/static/images/ jiaxin@114.113.154.46:/data/www/core/static/v3/images/
#rsync -avz --delete raspberry/base/static/font-awesome/ jiaxin@114.113.154.46:/data/www/core/static/v3/font-awesome/
