'''
Created by auto_sdk on 2013-08-28 14:05:29
'''
from top.api.base import RestApi
class HanoiDataserviceWriteRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.app_name = None
		self.data = None
		self.params = None

	def getapiname(self):
		return 'taobao.hanoi.dataservice.write'
