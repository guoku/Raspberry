# coding=utf-8
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from urlparse import urlparse
import json
import re
import HTMLParser

from base.entity import Entity
from base.entity import Note
from base.user import User
from base.item import Item
from base.category import Category
from base import fetcher


def _parse_taobao_id_from_url(url):
    params = url.split("?")[1]

    for param in params.split("&"):
        tokens = param.split("=")

        if len(tokens) >= 2 and (tokens[0] == "id" or tokens[0] == "item_id"):
            return tokens[1]

    return None


def _load_taobao_item_info(taobao_id):
    taobao_item_info = fetcher.fetch_item(taobao_id)
    thumb_images = []

    for _img_url in taobao_item_info["imgs"]:
        thumb_images.append(_img_url)

    taobao_item_info["thumb_images"] = thumb_images
    taobao_item_info["title"] = HTMLParser.HTMLParser().unescape(taobao_item_info["desc"])
    taobao_item_info["shop_nick"] = taobao_item_info["nick"]

    return taobao_item_info


@login_required
def load_entity(request, template='entity/create_entity.html'):
    _user = User(request.user.id)
    _user_context = _user.read()

    if request.method == 'GET':
        return render_to_response(
            template,
            {
                'is_post' : False,
                'user_context' : _user_context
            },
            context_instance = RequestContext(request)
        )

    else:
        _cand_url = request.POST.get("url", None)
        _hostname = urlparse(_cand_url).hostname

        if re.search(r"\b(tmall|taobao)\.com$", _hostname) is not None:
            _taobao_id = _parse_taobao_id_from_url(_cand_url)
            _item = Item.get_item_by_taobao_id(_taobao_id)

            if _item is None:
                _taobao_item_info = _load_taobao_item_info(_taobao_id)
                _chief_image_url = _taobao_item_info["thumb_images"][0]
                _selected_category_id = Category.get_category_by_taobao_cid(_taobao_item_info['cid'])

                return render_to_response(
                    template,
                    {
                        'is_post' : True,
                        'user_context' : _user_context,

                        'cand_url' : _cand_url,
                        'taobao_id': _taobao_id,
                        'cid': _taobao_item_info['cid'],
                        'taobao_title': _taobao_item_info['title'],
                        'shop_nick': _taobao_item_info['shop_nick'],
                        'price': _taobao_item_info['price'],
                        'chief_image_url' : _chief_image_url,
                        'thumb_images': _taobao_item_info["thumb_images"],
                        'selected_category_id': _selected_category_id,
                        'category_list': Category.find(),
                    },
                    context_instance=RequestContext(request)
                )

            elif _item.get_entity_id() == -1:
                return HttpResponse('已经入库')
            else:
                return HttpResponse('已经添加')


@login_required
def create_entity(request):
    if request.method == 'POST':
        _user_id = request.user.id

        # 只需要获取允许用户更改的数据
        _cand_url = request.POST.get('url', None)
        _brand = request.POST.get("brand", None)
        _title = request.POST.get("title", None)
        _chief_image_url = request.POST.get("chief_image_url", None)
        _note = request.POST.get("note_text", "")

        _hostname = urlparse(_cand_url).hostname

        if re.search(r"\b(tmall|taobao)\.com$", _hostname) is not None:
            _taobao_id = _parse_taobao_id_from_url(_cand_url)
            _item = Item.get_item_by_taobao_id(_taobao_id)

            if _item is None:
                _taobao_item_info = _load_taobao_item_info(_taobao_id)

                _category_id = Category.get_category_by_taobao_cid(_taobao_item_info['cid'])
                _detail_image_urls = _taobao_item_info["thumb_images"]

                if _chief_image_url in _detail_image_urls:
                    _detail_image_urls.remove(_chief_image_url)
                else:
                    # 确保 url 正确合法
                    _chief_image_url = _detail_image_urls[0]
                    _detail_image_urls.pop(0)

                _entity = Entity.create_by_taobao_item(
                    creator_id = _user_id,
                    category_id = _category_id,
                    chief_image_url = _chief_image_url,
                    taobao_item_info = {
                        'taobao_id': _taobao_id,
                        'cid': _taobao_item_info['cid'],
                        'title': _taobao_item_info['title'],
                        'shop_nick': unicode(_taobao_item_info['shop_nick'], 'utf-8'),  # 非unicode
                        'price': _taobao_item_info['price'],
                        'soldout': False,
                    },
                    brand = _brand,
                    title = _title,
                    detail_image_urls = _detail_image_urls,
                )

                _entity.add_note(creator_id=_user_id, note_text=_note)
                _entity_hash = _entity.read()['entity_hash']

                return HttpResponseRedirect(reverse('web_detail', kwargs = { "entity_hash" : _entity_hash }))


@login_required
def like_entity(request, entity_id):
    if request.method == 'POST':
        _user_id = request.user.id
        _entity = Entity(int(entity_id))

        if _entity.like_already(_user_id):
            _entity.unlike(_user_id)
            return HttpResponse('0')
        else:
            _entity.like(_user_id)
            return HttpResponse('1')


def get_notes(request, entity_id, template='entity/entity_note_list.html'):
    if request.method == 'GET':
        _user_context = User(request.user.id).read()
        _note_id_list = Note.find(entity_id=entity_id)
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

        if _note_text is not None and len(_note_text) > 0:
            _entity = Entity(int(entity_id))
            _note = _entity.add_note(request.user.id, _note_text)
            _note_context = _note.read()
            _user_context = User(request.user.id).read()

            return render_to_response(
                template,
                {
                    'note_context': _note_context,
                    'creator_context': _user_context,
                    'user_context': _user_context
                },
                context_instance = RequestContext(request)
            )


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
        pass