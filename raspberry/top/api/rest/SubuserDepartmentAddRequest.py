'''
Created by auto_sdk on 2013-11-15 12:58:10
'''
from top.api.base import RestApi
class SubuserDepartmentAddRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.department_name = None
		self.parent_id = None
		self.user_nick = None

	def getapiname(self):
		return 'taobao.subuser.department.add'
