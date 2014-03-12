# coding=utf8
import re
from urlparse import urlparse

def get_taobao_url(taobao_id, is_mobile = False, app_key = None):
    if is_mobile:
        url = "http://a.m.tmall.com/i%s.htm" % taobao_id
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
    hostname = urlparse(item_url).hostname
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

