'''
Created by auto_sdk on 2013-08-28 14:05:29
'''
from top.api.base import RestApi
class TaobaokeMobileItemsEliteGetRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.area = None
		self.ecat = None
		self.end_credit = None
		self.end_discount_rate = None
		self.end_price = None
		self.fields = None
		self.outer_code = None
		self.page_size = None
		self.postage_free = None
		self.q = None
		self.shop_type = None
		self.size = None
		self.start_credit = None
		self.start_discount_rate = None
		self.start_price = None

	def getapiname(self):
		return 'taobao.taobaoke.mobile.items.elite.get'
