'''
Created by auto_sdk on 2013-11-15 12:58:10
'''
from top.api.base import RestApi
class LogisticsOrdersDetailGetRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.buyer_nick = None
		self.end_created = None
		self.fields = None
		self.freight_payer = None
		self.page_no = None
		self.page_size = None
		self.receiver_name = None
		self.seller_confirm = None
		self.start_created = None
		self.status = None
		self.tid = None
		self.type = None

	def getapiname(self):
		return 'taobao.logistics.orders.detail.get'
