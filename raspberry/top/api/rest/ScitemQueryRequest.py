'''
Created by auto_sdk on 2013-11-15 12:58:10
'''
from top.api.base import RestApi
class ScitemQueryRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.bar_code = None
		self.item_name = None
		self.item_type = None
		self.outer_code = None
		self.page_index = None
		self.page_size = None
		self.wms_code = None

	def getapiname(self):
		return 'taobao.scitem.query'
