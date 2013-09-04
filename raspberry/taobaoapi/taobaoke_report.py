from top.api import TaobaokeReportGetRequest
from top import appinfo
import json

class TaobaokeReport():
    ALL_FIELDS = "trade_parent_id,trade_id,real_pay_fee,commission_rate,commission,app_key,outer_code,create_time,pay_time,pay_price,num_iid,item_title,item_num,category_id,category_name,shop_title,seller_nick"

    def __init__(self, app_key, app_secret):
        self.req = TaobaokeReportGetRequest()
        self.req.set_app_info(appinfo(app_key, app_secret))

    def get_taobaoke_report(self, date, page_no, page_size, fields = None):
        if not fields:
            self.req.fields = self.ALL_FIELDS
        else:
            self.req.fields = fields
        self.req.date = date
        self.req.page_no = page_no
        self.req.page_size = page_size
        try:
            resp = self.req.getResponse()
            return resp
        except Exception, e:
            return None
