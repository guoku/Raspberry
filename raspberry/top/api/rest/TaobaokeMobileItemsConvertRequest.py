'''
Created by auto_sdk on 2013-08-28 14:05:29
'''
from top.api.base import RestApi
class TaobaokeMobileItemsConvertRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.fields = None
		self.num_iids = None
		self.outer_code = None

	def getapiname(self):
		return 'taobao.taobaoke.mobile.items.convert'