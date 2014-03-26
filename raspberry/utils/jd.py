#encoding=utf8
import re
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
