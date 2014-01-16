# coding=utf8
from base.models import Log
from mongoengine import * 
import datetime

class MobileLogPrev(EmbeddedDocument):
    view = StringField(required = True)
    attributes = DictField(required = False)
    meta = {
        'indexes' : [ 
            'view'
        ]
    }

class MobileLog(Log):
    view = StringField(required = True)
    version = StringField(required = True)
    device = StringField(required = False)
    duid = StringField(required = False)
    os = StringField(required = False)
    prev = EmbeddedDocumentField(MobileLogPrev, required = False) 
    meta = {
        'indexes' : [ 
            'view', 
            'version', 
            'device',
            'duid',
            'os',
            'prev',
        ]
    }

def _gen_prev(prev_str):
    _tokens = prev_str.split('_')
    _view = _tokens[0].upper()
    _attributes = None
    if _view == 'SEARCH':
        _attributes = { 'query' : _tokens[1] }

    if _view in ['ENTITY', 'NOTE']:
        _attributes = { 'id' : int(_tokens[1]) }

    if _view in ['POPULAR', 'FEED']:
        _attributes = { 'block' : _tokens[1] }

    if _view == 'TAG':
        _attributes = { 'tag' : _tokens[1] }
    
    if _view in ['CATEGORY', 'USER']:
        _attributes = {
            'id' : _tokens[1],
            'block' : _tokens[2]
        }

    if _view == 'DISCOVER':
        _attributes = {
            'block' : _tokens[1]
        }
        if _tokens[1] == 'GROUP':
            _attributes['group_id'] = int(_tokens[2])

    if _view == 'EXTERNAL':
        _attributes = { 'source' : _tokens[1] }

        

    _prev_doc = MobileLogPrev(
        view = _view,
    )
    if _attributes != None:
        _prev_doc.attributes = _attributes
    return _prev_doc

def log(view, version, ip, request_user_id = None, device = None, duid = None, os = None, prev_str = None):
    _doc = MobileLog(
        entry = 'mobile',
        ip = ip,
        view = view.upper(),
        version = version,
        log_time = datetime.datetime.now()
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
    if _doc.view in ['ENTITY', 'CATEGORY'] and prev_str != None:
        _doc.prev = _gen_prev(prev_str)
    _doc.save()
