'''
Created by auto_sdk on 2013-11-15 12:58:10
'''
from top.api.base import RestApi
class HanoiGroupLabelDeleteRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.app_name = None
		self.group_id = None
		self.label_id = None

	def getapiname(self):
		return 'taobao.hanoi.group.label.delete'
