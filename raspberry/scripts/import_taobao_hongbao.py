import os, sys
sys.path.append('/data/www/raspberry')
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings.production'


from base.models import Event_Hongbao
# import csv


# datareader = csv.reader(open('test.csv'), delimiter=',', quotechar='"')
#
# for row in datareader:
#     hongbao = Event_Hongbao()
#     hongbao.qrcode = row[1]
#     hongbao.expires_in = '2014-12-13'
#     hongbao.save()


lines = [line.strip() for line in open('qrcode')]

for row in lines[0:6900]:
    hongbao = Event_Hongbao()
    hongbao.qrcode = row
    hongbao.expires_in = '2014-12-08'
    hongbao.save()
    # print row
    # print '2014-12-08'

for row in lines[6900:12900]:
    hongbao = Event_Hongbao()
    hongbao.qrcode = row
    hongbao.expires_in = '2014-12-09'
    hongbao.save()

for row in lines[12900:]:
    hongbao = Event_Hongbao()
    hongbao.qrcode = row
    hongbao.expires_in = '2014-12-10'
    hongbao.save()

__author__ = 'edison'
