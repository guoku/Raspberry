# coding=utf-8
from django.http import Http404, HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from utils.paginator import Paginator
from base.models import NoteSelection
from base.note import Note
from base.entity import Entity
from base.user import User
from base.category import Old_Category
from util import *


def selection(request, template='main/selection.html'):
    _user = get_request_user(request.user.id)
    _user_context = get_request_user_context(_user)
    _old_category_list = Old_Category.find()[0:12]

    _page_num = int(request.GET.get('p', 1))
    _category_id = request.GET.get('c', None)

    # 判断是否ajax方式加载,如不是则强制返回首页
    # 见https://docs.djangoproject.com/en/dev/ref/request-response/#django.http.HttpRequest.is_ajax
    if not request.is_ajax():
        _page_num = 1

    if _category_id is None:
        _hdl = NoteSelection.objects.all()
    else:
        _category_id = int(_category_id)
        _hdl = NoteSelection.objects.filter(category_id=_category_id)

    _total_count = _hdl.count()
    _count_in_one_page = 24
    _paginator = Paginator(_page_num, _count_in_one_page, _total_count)

    _hdl.order_by('-post_time')
    _offset = _paginator.offset
    _note_selection_list = _hdl[_offset: _offset + _count_in_one_page]

    _selection_list = []

    for _note_selection in _note_selection_list:
        _selection_note_id = _note_selection['note_id']
        _entity_id = _note_selection['entity_id']
        _entity_context = Entity(_entity_id).read()

        _note = Note(_selection_note_id)
        _note_context = _note.read()
        _creator_context = User(_note_context['creator_id']).read()
        _is_user_already_like = user_already_like_entity(request.user.id, _entity_id)

        _selection_list.append(
            {
                'is_user_already_like': _is_user_already_like,
                'entity_context': _entity_context,
                'note_context': _note_context,
                'creator_context': _creator_context,
            }
        )

    # 判断是否第一次加载
    if _page_num is None or _page_num == 1:
        return render_to_response(
            template,
            {
                'main_nav_deliver' : 'selection',
                'page_num' : _page_num,
                'curr_category_id' : _category_id,

                'user_context' : _user_context,
                'category_list' : _old_category_list,
                'selection_list' : _selection_list,
            },
            context_instance = RequestContext(request)
        )

    else:
        # 返回html片段
        return render_to_response(
            'main/partial/selection_item_list.html',
            {
                'selection_list' : _selection_list,
            },
            context_instance = RequestContext(request)
        )


def detail(request, entity_hash, template='main/detail.html'):
    _user = get_request_user(request.user.id)
    _user_context = get_request_user_context(_user)

    _entity_id = Entity.get_entity_id_by_hash(entity_hash)
    _entity_context = Entity(_entity_id).read()
    _note_id_list = Note.find(entity_id=_entity_id)

    _selection_note = None
    _common_note_list = []
    _user_already_note = False
    _already_like = user_already_like_entity(request.user.id, _entity_id)

    for _note_id in _note_id_list:
        _note = Note(_note_id)
        _note_context = _note.read()
        _creator_context = User(_note_context['creator_id']).read()

        if _creator_context['user_id'] == request.user.id:
            _user_already_note = True

        # 判断是否是精选
        if _note_context['is_selected']:
            _selection_note = {
                'note_context' : _note_context,
                'creator_context' : _creator_context,
                'user_context' : _user_context
            }
        else:
            _common_note_list.append(
                {
                    'note_context' : _note_context,
                    'creator_context' : _creator_context,
                    'user_context' : _user_context
                }
            )

    return render_to_response(
        template,
        {
            'user_context' : _user_context,
            'user_already_note' : _user_already_note,
            'entity_context' : _entity_context,
            'selection_note' : _selection_note,
            'common_note_list' : _common_note_list,
            'already_like' : _already_like
        },
        context_instance=RequestContext(request)
    )


def popular(request, template='main/popular.html'):
    _user = get_request_user(request.user.id)
    _user_context = get_request_user_context(_user)
    _group = request.GET.get('group', 'daily')

    # 先用精选数据来模拟热门 TODO
    _entity_id_list = map(lambda x: x['entity_id'], NoteSelection.objects.all()[0:30])
    _popular_list = []

    for _id in _entity_id_list:
        _entity = Entity(_id)
        _entity_context = _entity.read()
        _s_note_context = None
        _s_creator_context = None
        _note_id_list = Note.find(entity_id=_id)

        _already_like = user_already_like_entity(request.user.id, _id)

        # 找到精选点评 需优化? TODO
        for _note_id in _note_id_list:
            _note_context = Note(_note_id).read()
            if _note_context['is_selected']:
                _s_note_context = _note_context
                break

        if _s_note_context is not None:
            _s_creator_context = User(_s_note_context['creator_id']).read()

        _popular_list.append({
            'already_like' : _already_like,
            'entity_context' : _entity_context,
            's_note_context' : _s_note_context,
            's_creator_context' : _s_creator_context
        })

    return render_to_response(
        template,
        {
            'main_nav_deliver' : 'popular',
            'user_context' : _user_context,
            'popular_list' : _popular_list
        },
        context_instance=RequestContext(request)
    )


def discover(request, template='main/discover.html'):
    _user = get_request_user(request.user.id)
    _user_context = get_request_user_context(_user)

    # 先用精选数据来模拟 TODO
    _product_list = map(lambda x: Entity(x['entity_id']).read(), NoteSelection.objects.all()[0:10])

    return render_to_response(
        template,
        {
            'main_nav_deliver' : 'discover',
            'user_context' : _user_context,
            'product_list' : _product_list
        },
        context_instance=RequestContext(request)
    )


def discover_more(request):
    pass


def shop(request, shop_id):
    pass


def message(request, template='main/message.html'):
    if request.method == 'GET':
        _user = User(request.user.id)
        _user_context = _user.read()

        # TODO

        return render_to_response(
            template,
            {
                'user_context': _user_context,
            },
            context_instance = RequestContext(request)
        )


def activity(request, template='main/activity.html'):
    if request.method == "GET":
        _user = User(request.user.id)
        _user_context = _user.read()

        # TODO

        return render_to_response(
            template,
            {
                'user_context': _user_context,
            },
            context_instance = RequestContext(request)
        )
