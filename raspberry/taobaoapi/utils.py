from django.conf import settings
from item import TaobaoItem
from shop import TaobaoShop
from taobaoke_report import TaobaokeReport
from taobaoke import TaobaokeMobileItem
import json

APP_KEY = getattr(settings, "TAOBAO_APP_KEY", None)
APP_SECRET = getattr(settings, "TAOBAO_APP_SECRET", None)
CALLBACK_URL = getattr(settings, "TAOBAO_BACK_URL", None)
OAUTH_URL = getattr(settings, "TAOBAO_OAUTH_URL", None)
OAUTH_LOGOFF_URL = getattr(settings, "TAOBAO_OAUTH_LOGOFF", None)

def load_taobao_item_info_from_api(taobao_id):
    taobao = TaobaoItem(APP_KEY, APP_SECRET)
    res = taobao.get_item(taobao_id)
    try:
        return res['item_get_response']['item']
    except:
        return None

def load_taobao_shop_info_from_api(shop_nick):
    shop = TaobaoShop(APP_KEY, APP_SECRET)
    return shop.get_shop_info(shop_nick)

def load_taobaoke_report(date):
    report = TaobaokeReport(APP_KEY, APP_SECRET)
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

def taobaoke_mobile_item_convert(num_iid, outer_code, fields = None):
    request = TaobaokeMobileItem(APP_KEY, APP_SECRET)
    print "get"
    res = request.convert_items(num_iid, outer_code)
    print res
    try:
        return res['taobaoke_mobile_items_convert_response']['taobaoke_items']['taobaoke_item'][0]
    except:
        return None
    
