'''
Created by auto_sdk on 2013-08-28 14:05:29
'''
from top.api.base import RestApi
class HanoiAttributesGetRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.code = None
		self.current_page = None
		self.id = None
		self.indistinct_query = None
		self.page_size = None
		self.title = None
		self.top_access = None
		self.type_id = None
		self.type_name = None

	def getapiname(self):
		return 'taobao.hanoi.attributes.get'
