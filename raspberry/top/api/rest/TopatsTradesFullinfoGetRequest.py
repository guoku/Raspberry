'''
Created by auto_sdk on 2013-08-28 14:05:29
'''
from top.api.base import RestApi
class TopatsTradesFullinfoGetRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.fields = None
		self.tids = None

	def getapiname(self):
		return 'taobao.topats.trades.fullinfo.get'
