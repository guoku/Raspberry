'''
Created by auto_sdk on 2013-08-28 14:05:29
'''
from top.api.base import RestApi
class HanoiFunctionAddRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.app_name = None
		self.name = None
		self.parse_type = None
		self.rule = None
		self.strategy = None

	def getapiname(self):
		return 'taobao.hanoi.function.add'
