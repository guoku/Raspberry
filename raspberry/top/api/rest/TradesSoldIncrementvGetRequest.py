'''
Created by auto_sdk on 2013-11-15 12:58:10
'''
from top.api.base import RestApi
class TradesSoldIncrementvGetRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.end_create = None
		self.ext_type = None
		self.fields = None
		self.page_no = None
		self.page_size = None
		self.start_create = None
		self.status = None
		self.tag = None
		self.type = None
		self.use_has_next = None

	def getapiname(self):
		return 'taobao.trades.sold.incrementv.get'
