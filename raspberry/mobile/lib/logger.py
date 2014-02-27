# coding=utf8
from base.models import Log
from mongoengine import * 
import datetime

class MobileLogPrev(EmbeddedDocument):
    view = StringField(required = True)
    appendix = DictField(required = False)

class MobileLog(Log):
    view = StringField(required = True)
    version = StringField(required = True)
    device = StringField(required = False)
    duid = StringField(required = False)
    os = StringField(required = False)
    prev = EmbeddedDocumentField(MobileLogPrev, required = False) 

def _gen_prev(prev_str):
    _tokens = prev_str.split('_')
    _view = _tokens[0].upper()
    _appendix = None
    if _view == 'SEARCH':
        _appendix = { 'query' : _tokens[1] }

    if _view in ['ENTITY', 'NOTE']:
        _appendix = { 'id' : int(_tokens[1]) }

    if _view in ['POPULAR', 'FEED']:
        _appendix = { 'scale' : _tokens[1] }

    if _view == 'TAG':
        _appendix = { 'tag' : _tokens[1] }
    
    if _view in ['CATEGORY_ENTITY', 'USER']:
        _appendix = {
            'id' : _tokens[1],
            'block' : _tokens[2]
        }

    if _view == 'DISCOVER' and len(_tokens) > 1:
        _appendix = {
            'block' : _tokens[1]
        }
        if _tokens[1] == 'GROUP':
            _appendix['group_id'] = int(_tokens[2])

    if _view == 'EXTERNAL':
        _appendix = { 'source' : _tokens[1] }

        

    _prev_doc = MobileLogPrev(
        view = _view,
    )
    if _appendix != None:
        _prev_doc.appendix = _appendix
    return _prev_doc

def log(duration, view, version, ip, request_user_id = None, device = None, duid = None, os = None, prev_str = None, appendix = None):
    _doc = MobileLog(
        entry = 'mobile',
        duration = duration,
        ip = ip,
        view = view.upper(),
        version = version,
        log_time = datetime.datetime.now(),
    )
    if request_user_id == None:
        _doc.user_id = -1
    else:
        _doc.user_id = int(request_user_id)
    if device != None:
        _doc.device = device
    if duid != None:
        _doc.duid = duid
    if os != None:
        _doc.os = os
    if _doc.view in ['ENTITY', 'CATEGORY_ENTITY'] and prev_str != None:
        _doc.prev = _gen_prev(prev_str)
    if appendix != None:
        _doc.appendix = appendix
    _doc.save()
