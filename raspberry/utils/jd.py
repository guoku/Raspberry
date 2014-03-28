#encoding=utf8
import re
import HTMLParser
from utils.extractor.jd import JDExtractor
def get_jd_url(jd_id, is_mobile = False, app_key = None):
    jd_id = str(jd_id)
    url = ""
    if is_mobile:
        url = "http://m.jd.com/product/%s.html"%jd_id 
    else:
        url = "http://item.jd.com/%s.html"%jd_id
        if app_key:
            #这里需要根据京东的数据进行修改
            pass
    return url

def parse_jd_id_from_url(url):
    ids = re.findall(r'\d+',url)
    if len(ids) > 0:
        return ids[0]
    else:
        return None

def load_jd_item_info(jd_id):
    jd_item_info = JDExtractor.fetch_item(jd_id)
    thumb_images = []
    image_url = None
    for _img_url in jd_item_info["imgs"]:
        thumb_images.append(_img_url)
    jd_item_info['thumb_images'] = thumb_images
    jd_item_info['title'] = HTMLParser.HTMLParser().unescape(jd_item_info['desc'])
    jd_item_info['shop_nick'] = jd_item_info['nick']
    return jd_item_info
