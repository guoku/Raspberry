# coding=utf-8
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.shortcuts import render_to_response
from django.views.decorators.http import require_GET, require_POST
from django.template import RequestContext
from django.utils.log import getLogger
from django.template import loader
from urlparse import urlparse
import datetime 
import json
import re
import HTMLParser

from base.entity import Entity
from base.entity import Note
from base.user import User
from base.item import Item, JDItem
from base.tag import Tag 
from base.category import Category
from base.taobao_shop import GuokuPlusActivity
from share.tasks import CreateTaobaoShopTask
from share.tasks import CreateTaobaoShopTask, DeleteEntityNoteTask, LikeEntityTask, UnlikeEntityTask
from web.tasks import WebLogTask
from utils.extractor.taobao import TaobaoExtractor 
from utils.extractor.jd import JDExtractor
from utils.taobao import parse_taobao_id_from_url, load_taobao_item_info
from utils.lib import get_client_ip
from utils.jd import parse_jd_id_from_url, load_jd_item_info

log = getLogger('django')


def entity_detail(request, entity_hash, template='main/detail.html'):
    # _user_agent = request.META['HTTP_USER_AGENT']
    # if _user_agent == None:
    #     log.error("[selection] Remote Host [%s] access selection without user agent" % (request.META['REMOTE_ADDR']))
    #     raise Http404
    #
    # _agent = request.GET.get('agent', 'default')
    # if _agent == 'default' :
    #     if 'iPhone' in _user_agent :
    #         _agent = 'iphone'
    #     if 'Android' in _user_agent :
    #         _agent = 'android'
    # if _agent == 'iphone' or _agent == 'android' :
    #     return HttpResponseRedirect(reverse('wap_detail', kwargs = { "entity_hash" : entity_hash }))
    
    # _start_at = datetime.datetime.now()
    if request.user.is_authenticated():
        # _request_user_id = request.user.id
        _is_staff = request.user.is_staff
        _request_user_context = User(request.user.id).read() 
        _request_user_like_entity_set = Entity.like_set_of_user(request.user.id)
        _request_user_poke_note_set = Note.poke_set_of_user(request.user.id)
    else:
        # _request_user_id = None
        _is_staff = False 
        _request_user_context = None
        _request_user_like_entity_set = []
        _request_user_poke_note_set = []

    _entity_id = Entity.get_entity_id_by_hash(entity_hash)
    if _entity_id is None:
        raise Http404
    _entity_context = Entity(_entity_id).read()
    # log.info(_entity_context)
    _liker_list = Entity(_entity_id).liker_list(offset=0, count=20)
    _is_user_already_like = True if _entity_id in _request_user_like_entity_set else False
    _tag_list = Tag.entity_tag_stat(_entity_id)
    
    
    _is_soldout = True
    _taobao_id = None
    _jd_id = None
    _activity_id = None
    for _item_id in Item.find(entity_id=_entity_id):
        _item_context = Item(_item_id).read()
        if _item_context == None:
            _item_context = JDItem(_item_id).read()
            _jd_id = _item_context['jd_id']
            if not _item_context['soldout']:
                _is_soldout = False
        else:
            _taobao_id = _item_context['taobao_id']
            if not _item_context['soldout']:
                _is_soldout = False
                break
    if _taobao_id != None:
        try:
            _guokuplus = GuokuPlusActivity.find_by_taobao_id(_taobao_id)
            if _guokuplus != None and _guokuplus.is_active():
                _activity_id = _guokuplus.read()['activity_id']
        except Exception, e:
            pass
    
    _is_user_already_note = False
    if _request_user_context != None:
        _request_user_note_id_list = Note.find(entity_id=_entity_id, creator_set=[_request_user_context['user_id']])
        if len(_request_user_note_id_list) > 0:
            _is_user_already_note = True
    _selection_note = None
    _common_note_list = []
    for _note_id in Note.find(entity_id=_entity_id, sort_by='poke'):
        try:
            _note = Note(_note_id)
            _note_context = _note.read()
            if _note_context['weight'] >= 0:
                _creator_context = User(_note_context['creator_id']).read()
                _poke_button_target_status = '0' if _note_id in _request_user_poke_note_set else '1' 
                if _note_context['is_selected']:
                    _selection_note = {
                        'note_context' : _note_context,
                        'creator_context' : _creator_context,
                        'user_context' : _request_user_context,
                        'poke_button_target_status' : _poke_button_target_status,
                    }
                else:
                    _common_note_list.append({
                        'note_context' : _note_context,
                        'creator_context' : _creator_context,
                        'user_context' : _request_user_context,
                        'poke_button_target_status' : _poke_button_target_status,
                    })
        except Exception, e:
            log.error(e.message)
            # pass

    _guess_entity_context = []
    _guess_entity_id_list = []
    for _guess_entity_id in Entity.roll(category_id=_entity_context['category_id'], count=5):
        try:
            if _guess_entity_id != _entity_id: 
                _guess_entity_context.append(Entity(_guess_entity_id).read())
                _guess_entity_id_list.append(_entity_id)
                if len(_guess_entity_context) == 4:
                    break
        except Exception, e:
            log.error(e.message)
            # pass
    
    # _duration = datetime.datetime.now() - _start_at
    # WebLogTask.delay(
    #     duration=_duration.seconds * 1000000 + _duration.microseconds,
    #     page='ENTITY',
    #     request=request.REQUEST,
    #     ip=get_client_ip(request),
    #     log_time=datetime.datetime.now(),
    #     request_user_id=_request_user_id,
    #     appendix={
    #         'entity_id' : int(_entity_id),
    #         'guess_entities' : _guess_entity_id_list,
    #     },
    # )
    if _taobao_id != None: 
        return render_to_response(
            template,
            {
                'is_staff' : _is_staff,
                'user_context' : _request_user_context,
                'entity_context' : _entity_context,
                'is_user_already_note' : _is_user_already_note,
                'is_user_already_like' : _is_user_already_like,
                'selection_note' : _selection_note,
                'common_note_list' : _common_note_list,
                'liker_list' : _liker_list,
                'tag_list' : _tag_list,
                'guess_entity_context' : _guess_entity_context,
                'item_id' : _item_context['item_id'],
                'taobao_id' : _taobao_id,
                'activity_id' : _activity_id,
                'is_soldout' : _is_soldout,
                "enable_guoku_plus" : settings.ENABLE_GUOKU_PLUS
            },
            context_instance=RequestContext(request)
        )

    else:
        return render_to_response(
            template,
            {
                'is_staff' : _is_staff,
                'user_context' : _request_user_context,
                'entity_context' : _entity_context,
                'is_user_already_note' : _is_user_already_note,
                'is_user_already_like' : _is_user_already_like,
                'selection_note' : _selection_note,
                'common_note_list' : _common_note_list,
                'liker_list' : _liker_list,
                'tag_list' : _tag_list,
                'guess_entity_context' : _guess_entity_context,
                'item_id' : _item_context['item_id'],
                'jd_id' : _jd_id,
                'activity_id' : _activity_id,
                'is_soldout' : _is_soldout,
                "enable_guoku_plus" : settings.ENABLE_GUOKU_PLUS
            },
            context_instance=RequestContext(request)
        )

def wap_entity_detail(request, entity_hash, template='wap/detail.html'):
    _start_at = datetime.datetime.now()
    if request.user.is_authenticated():
        _request_user_id = request.user.id
    else:
        _request_user_id = None 
    
    
    _entity_id = Entity.get_entity_id_by_hash(entity_hash)
    _entity_context = Entity(_entity_id).read()
    
    _is_soldout = True
    _taobao_id = None
    _jd_id = None
    _is_jd = False
    for _item_id in Item.find(entity_id=_entity_id):
        _item_context = Item(_item_id).read()
        if _item_context == None:
            _item_context = JDItem(_item_id).read()
            _jd_id = _item_context['jd_id']
            _is_jd = True
        else:
            _taobao_id = _item_context['taobao_id']
        if not _item_context['soldout']:
            _is_soldout = False
            break
    
    _note_list = []
    for _note_id in Note.find(entity_id=_entity_id, reverse=True):
        _note = Note(_note_id)
        _note_context = _note.read()
        if _note_context['weight'] >= 0:
            _creator_context = User(_note_context['creator_id']).read()
            _note_list.append({
                'note_context' : _note_context,
                'creator_context' : _creator_context,
            })
    
    _liker_list = []
    for _liker in Entity(_entity_id).liker_list(offset=0, count=20):
        _liker_list.append(User(_liker[0]).read())
    
    # _duration = datetime.datetime.now() - _start_at
    # WebLogTask.delay(
    #     duration=_duration.seconds * 1000000 + _duration.microseconds,
    #     entry='wap',
    #     page='ENTITY',
    #     request=request.REQUEST,
    #     ip=get_client_ip(request),
    #     log_time=datetime.datetime.now(),
    #     request_user_id=_request_user_id,
    #     appendix={
    #         'entity_id' : int(_entity_id),
    #     },
    # )
    if _is_jd:
        buy_link = _item_context['buy_link']
        jd_id = parse_jd_id_from_url(buy_link)
        _item_context['buy_link'] = 'http://m.jd.com/product/%s.html' % jd_id
    return render_to_response(
        template,
        {
            'entity_context' : _entity_context,
            'note_list' : _note_list,
            'liker_list' : _liker_list,
            'buy_link' : _item_context['buy_link'],
            'is_jd' : _is_jd,
        },
        context_instance=RequestContext(request)
    )

def wechat_entity_detail(request, entity_id, template='wap/detail.html'):
    _start_at = datetime.datetime.now()
    if request.user.is_authenticated():
        _request_user_id = request.user.id
    else:
        _request_user_id = None 
    
    _entity_id = int(entity_id) 
    _entity_context = Entity(_entity_id).read()
    
    _is_soldout = True
    _taobao_id = None
    for _item_id in Item.find(entity_id=_entity_id):
        _item_context = Item(_item_id).read()
        _taobao_id = _item_context['taobao_id']
        if not _item_context['soldout']:
            _is_soldout = False
            break
    
    _note_list = []
    for _note_id in Note.find(entity_id=_entity_id, reverse=True):
        _note = Note(_note_id)
        _note_context = _note.read()
        if _note_context['weight'] >= 0:
            _creator_context = User(_note_context['creator_id']).read()
            _note_list.append({
                'note_context' : _note_context,
                'creator_context' : _creator_context,
            })
    
    _liker_list = []
    for _liker in Entity(_entity_id).liker_list(offset=0, count=20):
        _liker_list.append(User(_liker[0]).read())
    
    # _duration = datetime.datetime.now() - _start_at
    # WebLogTask.delay(
    #     duration=_duration.seconds * 1000000 + _duration.microseconds,
    #     entry='wechat',
    #     page='ENTITY',
    #     request=request.REQUEST,
    #     ip=get_client_ip(request),
    #     log_time=datetime.datetime.now(),
    #     request_user_id=_request_user_id,
    #     appendix={
    #         'entity_id' : int(_entity_id),
    #     },
    # )
    return render_to_response(
        template,
        {
            'entity_context' : _entity_context,
            'note_list' : _note_list,
            'liker_list' : _liker_list,
            'buy_link' : _item_context['buy_link'],
        },
        context_instance=RequestContext(request)
    )

def tencent_entity_detail(request, entity_hash, template='tencent/detail.html'):
    _start_at = datetime.datetime.now()
    if request.user.is_authenticated():
        _request_user_id = request.user.id
    else:
        _request_user_id = None 
    
    
    _entity_id = Entity.get_entity_id_by_hash(entity_hash)
    _entity_context = Entity(_entity_id).read()
    
    _is_soldout = True
    _taobao_id = None
    _jd_id = None
    _is_jd = False
    for _item_id in Item.find(entity_id=_entity_id):
        _item_context = Item(_item_id).read()
        if _item_context == None:
            _item_context = JDItem(_item_id).read()
            _jd_id = _item_context['jd_id']
            _is_jd = True
        else:
            _taobao_id = _item_context['taobao_id']
        if not _item_context['soldout']:
            _is_soldout = False
            break
    
    _note_list = []
    for _note_id in Note.find(entity_id=_entity_id, reverse=True):
        _note = Note(_note_id)
        _note_context = _note.read()
        if _note_context['weight'] >= 0:
            _creator_context = User(_note_context['creator_id']).read()
            _note_list.append({
                'note_context' : _note_context,
                'creator_context' : _creator_context,
            })
    
    _liker_list = []
    for _liker in Entity(_entity_id).liker_list(offset=0, count=20):
        _liker_list.append(User(_liker[0]).read())
    
    _duration = datetime.datetime.now() - _start_at
    WebLogTask.delay(
        duration=_duration.seconds * 1000000 + _duration.microseconds,
        entry='tencent',
        page='ENTITY', 
        request=request.REQUEST, 
        ip=get_client_ip(request), 
        log_time=datetime.datetime.now(),
        request_user_id=_request_user_id,
        appendix={ 
            'entity_id' : int(_entity_id),
        },
    )

    return render_to_response(
        template,
        {
            'entity_context' : _entity_context,
            'note_list' : _note_list,
            'liker_list' : _liker_list,
            'buy_link' : _item_context['buy_link'],
            'is_jd' : _is_jd,
        },
        context_instance=RequestContext(request)
    )


def jd_info(request, _cand_url):
    _jd_id = parse_jd_id_from_url(_cand_url)
    _item = JDItem.get_item_by_jd_id(_jd_id)
    _rslt = {}
    if _item == None:
        _jd_item_info = load_jd_item_info(_jd_id)
        _chief_image_url = _jd_item_info['thumb_images'][0]
        #TODO：进行京东类目转换
        #TODO :先用一个cid暂时使用着先
        cid = '1512' 
        _selected_category_id = Category.get_category_by_jd_cid(cid)
        _data = {
            'user_context' : User(request.user.id).read(),
            'cand_url' : _cand_url,
            'jd_id' : _jd_id,
            'jd_title' : _jd_item_info['title'],
            'shop_nick' : _jd_item_info['nick'],
            'shop_link' : _jd_item_info['shop_link'],
            'brand' : _jd_item_info['brand'],
            'price' : _jd_item_info['price'],
            'chief_image_url' :  _chief_image_url,
            'thumb_images' :[x.replace("/n1/", "/n5/") for x in  _jd_item_info['thumb_images']],
            'cid' : cid,
            'selected_category_id' : _selected_category_id,
            }
        _rslt = {
            'status' : 'SUCCESS',
            'data' : _data
            }
    elif _item.get_entity_id() == -1:
        _rslt = {
            'status' : 'OTHER'    
            }

    else:
        _entity_id = _item.get_entity_id()
        _entity_context = Entity(_entity_id).read()
        _rslt = {
                'status' : 'EXIST',
                'data' : {
                    'entity_hash' : _entity_context['entity_hash']
                    }
            }
    return HttpResponse(json.dumps(_rslt))


@login_required
def load_item_info(request):
    if request.method == 'POST':
        _cand_url = request.POST.get("cand_url", None)
        _hostname = urlparse(_cand_url).hostname

        if re.search(r"\b(jd|360buy)\.com$", _hostname) != None:
            return jd_info(request, _cand_url)

        if re.search(r"\b(tmall|taobao)\.com$", _hostname) is not None:
            _taobao_id = parse_taobao_id_from_url(_cand_url)
            _item = Item.get_item_by_taobao_id(_taobao_id)

            if _item is None:
                _taobao_item_info = load_taobao_item_info(_taobao_id)
                _chief_image_url = _taobao_item_info["thumb_images"][0]
                _selected_category_id = Category.get_category_by_taobao_cid(_taobao_item_info['cid'])
                _data = {
                    'user_context' : User(request.user.id).read(), 
                    'cand_url' : _cand_url,
                    'taobao_id': _taobao_id,
                    'cid': _taobao_item_info['cid'],
                    'taobao_title': _taobao_item_info['title'],
                    'shop_nick': _taobao_item_info['shop_nick'],
                    'shop_link': _taobao_item_info['shop_link'],
                    'price': _taobao_item_info['price'],
                    'chief_image_url' : _chief_image_url,
                    'thumb_images': _taobao_item_info["thumb_images"],
                    'selected_category_id': _selected_category_id,
                }
                _rslt = {
                    'status' : 'SUCCESS',
                    'data' : _data
                }
            elif _item.get_entity_id() == -1:
                _rslt = {
                    'status' : 'OTHER'
                }
            else:
                _entity_id = _item.get_entity_id()
                _entity_context = Entity(_entity_id).read()
                _rslt = {
                    'status' : 'EXIST',
                    'data' : {
                        'entity_hash' : _entity_context['entity_hash']
                    }
                }
            return HttpResponse(json.dumps(_rslt))


@login_required
def create_entity(request, template='entity/new_entity_from_user.html'):
    if request.method == 'GET':
        return render_to_response(
            template,
            {
            },
            context_instance = RequestContext(request)
        )
    else:
        _taobao_id = request.POST.get("taobao_id", None)
        if _taobao_id == None:
            return create_jd_entity(request,template)
        _cid = request.POST.get("cid", None)
        _taobao_shop_nick = request.POST.get("shop_nick", None)
        _taobao_shop_link = request.POST.get("shop_link", None)
        _taobao_title = request.POST.get("taobao_title", None)
        _taobao_price = float(request.POST.get("price", "0.0"))
        _chief_image_url = request.POST.get("chief_image_url", None)
        _brand = request.POST.get("brand", None)
        _title = request.POST.get("title", None)
        _note_text = request.POST.get("note_text", None)
        _user_id = request.POST.get("user_id", None)
        
        _intro = ""
        _category_id = int(request.POST.get("selected_category_id", "0"))
        _detail_image_urls = request.POST.getlist("thumb_images")
        
        if _chief_image_url in _detail_image_urls:
            _detail_image_urls.remove(_chief_image_url)
        
        _entity = Entity.create_by_taobao_item(
            creator_id=request.user.id,
            category_id=_category_id,
            chief_image_url=_chief_image_url,
            taobao_item_info={
                'taobao_id' : _taobao_id,
                'cid' : _cid,
                'title' : _taobao_title,
                'shop_nick' : _taobao_shop_nick,
                'price' : _taobao_price,
                'soldout' : False,
            },
            brand=_brand,
            title=_title,
            intro=_intro,
            detail_image_urls=_detail_image_urls,
            weight=-1
        )

        _note = _entity.add_note(creator_id=_user_id, note_text=_note_text)
        
        try:
            CreateTaobaoShopTask.delay(_taobao_shop_nick, _taobao_shop_link)
        except Exception, e:
            pass

        return HttpResponseRedirect(reverse('web_detail', kwargs = { "entity_hash" : _entity.get_entity_hash() }))


def create_jd_entity(request, template):
    _cid = request.POST.get("cid", None)
    _jd_id = request.POST.get("jd_id", None)
    _jd_shop_nick = request.POST.get("shop_nick", None)
    _jd_shop_link = request.POST.get("shop_link", None)
    _jd_title = request.POST.get("jd_title", None)
    _jd_price = float(request.POST.get("price", "0.0"))
    _chief_image_url = request.POST.get("chief_image_url", None)
    _brand = request.POST.get("brand", None)
    _title = request.POST.get("title", None)
    _note_text = request.POST.get("note_text", None)
    _user_id = request.POST.get("user_id", None)

    _intro = ""
    _category_id = int(request.POST.get("selected_category_id", "0"))
    _detail_image_urls = request.POST.getlist("thumb_images")

    if _chief_image_url in _detail_image_urls:
        _detail_image_urls.remove(_chief_image_url)

    _detail_image_urls = [x.replace("/n5/","/n1/") for x in _detail_image_urls]
    _entity = Entity.create_by_jd_item(
            creator_id = request.user.id,
            category_id = _category_id,
            chief_image_url = _chief_image_url,
            jd_item_info = {
                "jd_id" : _jd_id,
                "cid" : _cid,
                "title" : _jd_title,
                "shop_nick" : _jd_shop_nick,
                "price" : _jd_price,
                "soldout" : False,
            },
            brand = _brand,
            title = _title,
            intro = _intro,
            detail_image_urls = _detail_image_urls,
    )
    _note = _entity.add_note(creator_id = _user_id, note_text = _note_text)
    return HttpResponsePermanentRedirect(reverse('web_detail', kwargs = {"entity_hash" : _entity.get_entity_hash()}))


@login_required
def like_entity(request, entity_id, target_status):
    if request.is_ajax():
        if request.method == 'POST':
            _request_user_id = request.user.id
            if target_status == '1':
                LikeEntityTask.delay(entity_id, _request_user_id)
                return HttpResponse('1')
            else:
                UnlikeEntityTask.delay(entity_id, _request_user_id)
                return HttpResponse('0')
    else:
        raise Http404



def get_notes(request, entity_id, template='entity/entity_note_list.html'):
    if request.method == 'GET':
        _user_context = User(request.user.id).read()
        _note_id_list = Note.find(entity_id=entity_id, sort_by='poke')
        _note_list = []
        
        for _note_id in _note_id_list:
            _note = Note(_note_id)
            _note_context = _note.read()
            _creator_id = _note_context['creator_id']
            _creator_context = User(_creator_id).read()

            if not _note_context['is_selected']:
                _note_list.append(
                    {
                        'note_context' : _note_context,
                        'creator_context' : _creator_context,
                        'user_context' : _user_context
                    }
                )

        # TODO 需要改进 返回json 参照 main.selection
        return render_to_response(
            template,
            {
                'note_list' : _note_list
            },
            context_instance = RequestContext(request)
        )


@login_required
def add_note(request, entity_id, template='entity/entity_note.html'):
    if request.method == 'POST':
        _note_text = request.POST.get('note_text', None)
        _ret = {
            'status' : '0',
            'msg' : ''
        }

        if _note_text is not None and len(_note_text) > 0:
            _entity = Entity(int(entity_id))
            # TODO 连接有问题 正式需要替换以下两句
            _note = _entity.add_note(request.user.id, _note_text)
            # _note = Note(312868)
            _note_context = _note.read()
            _user_context = User(request.user.id).read()

            _t = loader.get_template(template)
            _c = RequestContext(request, {
                'note_context': _note_context,
                'creator_context': _user_context,
                'user_context': _user_context
            })
            _data = _t.render(_c)

            _ret = {
                'status' : '1',
                'data' : _data
            }

        return HttpResponse(json.dumps(_ret))


@login_required
def update_note(request, entity_id, note_id):
    if request.method == 'POST':
        _note_text = request.POST.get('note_text', None)

        if _note_text is not None and len(_note_text) > 0:
            _note_context = Note(note_id).read()

            # 判断当前用户是否具有修改权限
            if _note_context['creator_id'] == request.user.id:
                _entity = Entity(entity_id)
                _entity.update_note(note_id, note_text=_note_text)

                return HttpResponse('1')


@login_required
def delete_note(request, entity_id, note_id):
    if request.method == 'POST':
        # 暂时不需要该功能 以前版本没有
        pass

def log_visit_item(request, item_id):
    if request.user.is_authenticated():
        _request_user_id = request.user.id
    else:
        _request_user_id = None 
    if request.method == 'POST':
        _entry = request.POST.get("entry", "web")
        _item_id = request.POST.get("item_id", None) 
        _item_context = Item(item_id).read()
        _entity_id = _item_context['entity_id'] if _item_context.has_key('entity_id') else -1 
        # WebLogTask.delay(
        #     duration=0,
        #     entry='web',
        #     page='CLICK',
        #     request=request.REQUEST,
        #     ip=get_client_ip(request),
        #     log_time=datetime.datetime.now(),
        #     request_user_id=_request_user_id,
        #     appendix={
        #         'site' : 'taobao',
        #         'taobao_id' : _item_context['taobao_id'],
        #         'item_id' : item_id,
        #         'entity_id' : _entity_id,
        #     },
        # )
        return HttpResponse('1')

# coding=utf-8

