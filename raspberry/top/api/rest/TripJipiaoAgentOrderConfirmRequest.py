'''
Created by auto_sdk on 2013-08-28 14:05:29
'''
from top.api.base import RestApi
class TripJipiaoAgentOrderConfirmRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.order_id = None
		self.pnr_info = None

	def getapiname(self):
		return 'taobao.trip.jipiao.agent.order.confirm'