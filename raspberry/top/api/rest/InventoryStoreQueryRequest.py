'''
Created by auto_sdk on 2013-08-28 14:05:29
'''
from top.api.base import RestApi
class InventoryStoreQueryRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.store_code = None

	def getapiname(self):
		return 'taobao.inventory.store.query'
