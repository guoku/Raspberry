'''
Created by auto_sdk on 2013-08-28 14:05:29
'''
from top.api.base import RestApi
class PromotionmiscItemActivityDeleteRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.activity_id = None

	def getapiname(self):
		return 'taobao.promotionmisc.item.activity.delete'