'''
Created by auto_sdk on 2013-11-15 12:58:10
'''
from top.api.base import RestApi
class PromotionmiscMjsActivityAddRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.decrease_amount = None
		self.discount_rate = None
		self.end_time = None
		self.exclude_area = None
		self.gift_id = None
		self.gift_name = None
		self.gift_url = None
		self.is_amount_multiple = None
		self.is_amount_over = None
		self.is_decrease_money = None
		self.is_discount = None
		self.is_free_post = None
		self.is_item_count_over = None
		self.is_item_multiple = None
		self.is_send_gift = None
		self.is_shop_member = None
		self.is_user_tag = None
		self.item_count = None
		self.name = None
		self.participate_range = None
		self.shop_member_level = None
		self.start_time = None
		self.total_price = None
		self.type = None
		self.user_tag = None

	def getapiname(self):
		return 'taobao.promotionmisc.mjs.activity.add'
