'''
Created by auto_sdk on 2013-08-28 14:05:29
'''
from top.api.base import RestApi
class HanoiTypesGetRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.current_page = None
		self.id = None
		self.name = None
		self.page_size = None

	def getapiname(self):
		return 'taobao.hanoi.types.get'
