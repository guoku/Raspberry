from utils.taobao import is_taobao_url, parse_taobao_id_from_url
from utils.extractor.taobao import TaobaoExtractor 
from base.item import Item
from base.entity import Entity
from base.category import Category
import HTMLParser
class NotTaobaoUrl(Exception):
    def __init__(self):
        self.__message = "url is not a taobao url"
    def __str__(self):
        return repr(self.__message)

class NotSellerOwnProduct(Exception):
    def __init__(self):
        self.__message = "the item is not owned by this seller"
    def __str__(self):
        return repr(self.__message)

class InvalidUrl(Exception):
    def __init__(self):
        self.__message = "url is not valid"
    def __str__(self):
        return repr(self.__message)

def get_guoku_plus_item_context(taobao_url, shop_nick, user_id):
    if not is_taobao_url(taobao_url):
        raise NotTaobaoUrl()
    taobao_id = parse_taobao_id_from_url(taobao_url)
    if not taobao_id:
        raise InvalidUrl()
    
    item_inst = Item.get_item_by_taobao_id(taobao_id)
    if not item_inst:
        taobao_item_info = TaobaoExtractor.fetch_item(taobao_id)
        print taobao_item_info
        _category_id = Category.get_category_by_taobao_cid(taobao_item_info['cid'])
        _chief_image = None
        _detail_image_urls = []
        imgs_len = len(taobao_item_info['imgs'])
        if imgs_len > 0:
            _chief_image = taobao_item_info['imgs'][0]
            for i in range(1, imgs_len):
                _detail_image_urls.append(taobao_item_info['imgs'][i])
        _title = HTMLParser.HTMLParser().unescape(taobao_item_info['desc'])
        Entity.create_by_taobao_item(
            creator_id = user_id,
            category_id = _category_id,
            chief_image_url = _chief_image,
            taobao_item_info = {
                'taobao_id' : taobao_id,
                'cid' : taobao_item_info['cid'],
                'title' : _title,
                'shop_nick' : unicode(taobao_item_info['nick'], 'utf-8'),
                'price' : taobao_item_info['price'],
                'soldout' : False,
            },
            brand = "",
            title = _title,
            detail_image_urls = _detail_image_urls
        )
        item_inst = Item.get_item_by_taobao_id(taobao_id)
    item_context = item_inst.read()
    if item_context['shop_nick'] != shop_nick:
        raise NotSellerOwnProduct()
    return item_context
                

