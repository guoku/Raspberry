'''
Created by auto_sdk on 2013-11-15 12:58:10
'''
from top.api.base import RestApi
class TaobaokeMobileShopsConvertRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.fields = None
		self.outer_code = None
		self.seller_nicks = None
		self.sids = None

	def getapiname(self):
		return 'taobao.taobaoke.mobile.shops.convert'
