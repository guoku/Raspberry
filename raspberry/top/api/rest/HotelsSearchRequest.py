'''
Created by auto_sdk on 2013-11-15 12:58:10
'''
from top.api.base import RestApi
class HotelsSearchRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.city = None
		self.country = None
		self.district = None
		self.domestic = None
		self.name = None
		self.page_no = None
		self.province = None

	def getapiname(self):
		return 'taobao.hotels.search'
