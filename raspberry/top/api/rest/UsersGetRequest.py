'''
Created by auto_sdk on 2013-05-06 12:48:10
'''
from top.api.base import RestApi
class UsersGetRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.fields = None
		self.nicks = None

	def getapiname(self):
		return 'taobao.users.get'