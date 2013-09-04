'''
Created by auto_sdk on 2013-08-28 14:05:29
'''
from top.api.base import RestApi
class TaobaokeMobileShopsRelateGetRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.fields = None
		self.max_count = None
		self.outer_code = None
		self.seller_id = None
		self.seller_nick = None
		self.shop_type = None
		self.sort = None

	def getapiname(self):
		return 'taobao.taobaoke.mobile.shops.relate.get'
