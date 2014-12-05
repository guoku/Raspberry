import os, sys
sys.path.append('/data/www/raspberry')
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings.production'


from base.models import Event_Hongbao
import csv


datareader = csv.reader(open('test.csv'), delimiter=',', quotechar='"')

for row in datareader:
    hongbao = Event_Hongbao()
    hongbao.qrcode = row[1]
    hongbao.expires_in = '2014-12-13'
    hongbao.save()

__author__ = 'edison'
