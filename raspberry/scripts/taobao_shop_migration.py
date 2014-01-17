from mongoengine import *
import pymongo

import sys
sys.path.append("..")
from base.stream_models import *

conn = pymongo.Connection(host='10.0.1.23', port=27017)

db = conn.mango
col = db.taobao_shops_depot

shops = col.find()

connect("guoku_01_17_8", host="localhost")
for shop in shops:
    _shop_info = shop.get('shop_info', None)
    if not _shop_info:
        print shop
        print "\n\n"
        continue
    shop_score = ShopScore(credit = _shop_info['shop_score']['credit'],
                           praise_rate = _shop_info['shop_score']['praise_rate'])
    shop_info = TaobaoShopInfo(
        cid = _shop_info['cid'],
        nick = _shop_info['nick'],
        pic_path = _shop_info['pic_path'],
        sid = _shop_info['sid'],
        title = _shop_info['title'],
        seller_id = _shop_info.get('seller_id', None),
        company = _shop_info['company'],
        shop_type = _shop_info.get('shop_type', None),
        shop_link = _shop_info.get('shop_link', None),
        shop_score = shop_score,
        main_products = _shop_info.get('main_products', None),
        location = _shop_info.get('location', None),
        updated_time = _shop_info.get('updated_time', None))
    crawler_info = CrawlerInfo(priority = shop['crawler_info']['priority'],
                               cycle = shop['crawler_info']['cycle'])
    extended_info = TaobaoShopExtendedInfo(
        orientational = shop['extended_info']['orientational'],
        commission_rate = shop['extended_info']['commission_rate'],
        commission = shop['extended_info']['commission'],
        single_tail = shop['extended_info']['single_tail'],
        gifts = shop['extended_info']['gifts'])
    taobao_shop = TaobaoShop(shop_info = shop_info,
                             created_time = shop['created_time'],
                             last_updated_time = shop['last_updated_time'],
                             last_crawled_time = shop['last_crawled_time'],
                             crawler_info = crawler_info,
                             extended_info = extended_info)

    taobao_shop.save()
