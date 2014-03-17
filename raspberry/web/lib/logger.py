# coding=utf8
from base.models import Log
from mongoengine import * 
import datetime

class WebLogPrev(EmbeddedDocument):
    page = StringField(required=True)
    appendix = DictField(required=False)

class WebLog(Log):
    page = StringField(required=True)
    prev = EmbeddedDocumentField(WebLogPrev, required=False) 

def _gen_prev(prev_str):
    _tokens = prev_str.split('_')
    _page = _tokens[0].upper()
    _appendix = None
    if _page == 'SEARCH':
        _appendix = { 'query' : _tokens[1] }

    if _page in ['ENTITY']:
        _appendix = { 'id' : Entity.get_entity_id_by_hash(_tokens[1]) }

    if _page in ['POPULAR']:
        _appendix = { 'scale' : _tokens[1] }

    if _page == 'TAG':
        _appendix = { 'tag' : _tokens[1] }
    
    if _page in ['USER']:
        _appendix = {
            'id' : _tokens[1],
            'block' : _tokens[2]
        }

    if _page == 'EXTERNAL':
        _appendix = { 'source' : _tokens[1] }
        

    _prev_doc = WebLogPrev(
        page = _page,
    )
    if _appendix != None:
        _prev_doc.appendix = _appendix
    return _prev_doc

def log(duration, page, ip, log_time, entry='web', request_user_id=None, prev_str=None, appendix=None):
    _doc = WebLog(
        entry=entry,
        duration=duration,
        ip=ip,
        page=page.upper(),
        log_time=log_time, 
    )
    if request_user_id == None:
        _doc.user_id = -1
    else:
        _doc.user_id = int(request_user_id)
    if _doc.page in ['ENTITY', 'CATEGORY_ENTITY'] and prev_str != None:
        _doc.prev = _gen_prev(prev_str)
    if appendix != None:
        _doc.appendix = appendix
    _doc.save()
