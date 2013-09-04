# coding=utf-8

from top.api import ItemcatsGetRequest
from top import appinfo
class TaobaoCate():
    def __init__(self, app_key, app_secret):
        self.req.ItemcatsGetRequest()
        self.req.set_app_info(appinfo(app_key, app_secret))

    def get_cate_by_parent_id(self, parent_cid):
        parent_cid = unicode(parent_cid)
        self.req.fields = 'cid, parent_cid, name, is_parent, status, sort_order'
        self.req.parent_cid = parent_cid
        return self.req.getResponse()
    
    def get_cate_by_cid(self, cid):
        cid = unicode(cid)
        self.req.fields = 'cid, parent_cid, name, is_parent, status, sort_order'
        self.req.cids = cid
        return self.req.getResponse()
