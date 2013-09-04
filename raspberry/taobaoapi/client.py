from django.conf import settings
from item import TaobaoItem
from shop import TaobaoShop
from taobaoke_report import TaobaokeReport
from taobaoke import TaobaokeMobileItem
import json

class TaobaoApiClient(object):
    def __init__(self, app_key, secret):
        self.app_key = app_key
        self.secret = secret

    def load_taobao_item_info(self, taobao_id):
        taobao = TaobaoItem(self.app_key, self.secret)
        res = taobao.get_item(taobao_id)
        try:
            return res['item_get_response']['item']
        except:
            return None

    def load_taobao_shop_info(shop_nick):
        shop = TaobaoShop(self.app_key, self.secret)
        return shop.get_shop_info(shop_nick)

    def load_taobaoke_report(self, date):
        report = TaobaokeReport(self.app_key, self.secret)
        page_no = 1
        page_size = 100
        result = []
        while True:
            resp = report.get_taobaoke_report(date, page_no, page_size)
            if not resp or not resp.has_key('taobaoke_report_get_response') or len(resp['taobaoke_report_get_response']) == 0:
                break
            try:
                result.extend(resp['taobaoke_report_get_response']['taobaoke_report']['taobaoke_report_members']['taobaoke_report_member'])
            except Exception, e:
                print e
                break
            page_no += 1
        return result

    def taobaoke_mobile_item_convert(self, num_iid, outer_code, fields = None):
        request = TaobaokeMobileItem(self.app_key, self.secret)
        res = request.convert_items(num_iid, outer_code)
        try:
            return res['taobaoke_mobile_items_convert_response']['taobaoke_items']['taobaoke_item'][0]
        except:
            return None
        
