'''
Created by auto_sdk on 2013-11-15 12:58:10
'''
from top.api.base import RestApi
class HanoiTemplateUpdateRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.app_name = None
		self.data_template_id = None
		self.description = None
		self.expression = None
		self.gmt_modified = None
		self.id = None
		self.name = None
		self.open = None
		self.para_list = None
		self.source_template_id = None
		self.template_code = None

	def getapiname(self):
		return 'taobao.hanoi.template.update'
