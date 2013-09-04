'''
Created by auto_sdk on 2013-08-28 14:05:29
'''
from top.api.base import RestApi
class VideoUpdateRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.cover_url = None
		self.description = None
		self.tags = None
		self.title = None
		self.video_app_key = None
		self.video_id = None

	def getapiname(self):
		return 'taobao.video.update'
