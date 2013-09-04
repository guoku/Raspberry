'''
Created by auto_sdk on 2013-08-28 14:05:29
'''
from top.api.base import RestApi
class TmallEaiOrderRefundGoodReturnAgreeRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.message = None
		self.refund_id = None
		self.refund_phase = None
		self.refund_version = None
		self.seller_logistics_address_id = None

	def getapiname(self):
		return 'tmall.eai.order.refund.good.return.agree'
