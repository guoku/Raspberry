# coding=utf8
import re
from urlparse import urlparse
from utils.extractor.taobao import TaobaoExtractor 
import HTMLParser

from django.utils.log import getLogger

log = getLogger('django')


def get_taobao_url(taobao_id, is_mobile = False, app_key = None):
    url = ""
    if is_mobile:
        url = "http://a.m.taobao.com/i%s.htm" % taobao_id
    else:
        url = "http://item.taobao.com/item.htm?id=%s" % taobao_id
        if app_key:
            url += "&spm=2014.%s.0.0" % app_key
    return url

def is_taobaoke_url(url):
    return "s.click.taobao.com" in url

def decorate_taobao_url(url, ttid=None, sid=None, outer_code=None, sche=None):
    if sche:
        question_mark = "" if "?" in url else "?"
        url += question_mark + "&sche=%s" % sche
    if ttid:
        question_mark = "" if "?" in url else "?"
        url += question_mark + "&ttid=%s" % ttid
    if sid:
        question_mark = "" if "?" in url else "?"
        url += question_mark + "&sid=%s" % sid
    if is_taobaoke_url(url) and outer_code:
        question_mark = "" if "?" in url else "?"
        url += question_mark + "&unid=%s" % outer_code
    
    return url

def is_taobao_url(url):
    hostname = urlparse(url).hostname
    if re.search(r"\b(tmall|taobao)\.(com|hk)$", hostname) != None:
        return True
    return False
    
def parse_taobao_id_from_url(url):
    params = url.split("?")[1]
    for param in params.split("&"):
        tokens = param.split("=")
        if len(tokens) >= 2 and (tokens[0] == "id" or tokens[0] == "item_id"):
            return tokens[1]
    return None


def load_taobao_item_info(taobao_id):
    taobao_item_info = TaobaoExtractor.fetch_item(taobao_id)
    log.info(taobao_item_info)
    thumb_images = []
    image_url = None
    for _img_url in taobao_item_info["imgs"]:
        thumb_images.append(_img_url)
    taobao_item_info["thumb_images"] = thumb_images
    taobao_item_info["title"] = HTMLParser.HTMLParser().unescape(taobao_item_info["desc"])
    
    taobao_item_info["shop_nick"] = taobao_item_info["nick"].decode("utf8")
     
    return taobao_item_info
