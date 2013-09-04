'''
Created by auto_sdk on 2013-08-28 14:05:29
'''
from top.api.base import RestApi
class WlbWaybillallocationRequestwaybillnumRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.num = None
		self.out_biz_code = None
		self.pool_type = None
		self.service_code = None
		self.user_id = None

	def getapiname(self):
		return 'taobao.wlb.waybillallocation.requestwaybillnum'
