'''
Created by auto_sdk on 2013-08-28 14:05:29
'''
from top.api.base import RestApi
class HanoiDatatemplateDetailDeleteRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.app_name = None
		self.data_template_detail_ids = None
		self.data_template_vo = None

	def getapiname(self):
		return 'taobao.hanoi.datatemplate.detail.delete'
