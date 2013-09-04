'''
Created by auto_sdk on 2013-08-28 14:05:29
'''
from top.api.base import RestApi
class TravelItemAddRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.approve_status = None
		self.auction_point = None
		self.cid = None
		self.city = None
		self.desc = None
		self.duration = None
		self.fee_include = None
		self.fee_not_include = None
		self.has_discount = None
		self.has_invoice = None
		self.has_showcase = None
		self.image = None
		self.is_tdcy = None
		self.list_time = None
		self.num = None
		self.order_info = None
		self.outer_id = None
		self.pic_path = None
		self.play_desc = None
		self.play_id = None
		self.price = None
		self.price_calendar = None
		self.props = None
		self.prov = None
		self.refund_regulation = None
		self.second_kill = None
		self.seller_cids = None
		self.sku_prices = None
		self.sku_properties = None
		self.sku_quantities = None
		self.sub_stock = None
		self.title = None

	def getapiname(self):
		return 'taobao.travel.item.add'

	def getMultipartParas(self):
		return ['image']
