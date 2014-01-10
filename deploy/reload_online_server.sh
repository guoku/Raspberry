#!/bin/bash

#FAB='/Users/edison7500/PycharmProjects/django15/bin/fab'
FAB=`which fab`

${FAB} -f reload_server.py reload

