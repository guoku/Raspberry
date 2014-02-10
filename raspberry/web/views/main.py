# coding=utf-8
from django.http import Http404, HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template import loader
import json
from utils.http import JSONResponse
from datetime import datetime

from utils.paginator import Paginator
from base.models import NoteSelection
from base.note import Note
from base.entity import Entity
from base.user import User
from base.category import Old_Category
from util import get_request_user, get_request_user_context, user_already_like_entity

def index(request):
    return HttpResponseRedirect(reverse('web_selection'))

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
        _hdl = NoteSelection.objects(post_time__lt = datetime.now())
    else:
        _category_id = int(_category_id)
        _hdl = NoteSelection.objects(category_id=_category_id, post_time__lt = datetime.now())
    _total_count = _hdl.count()
    _count_in_one_page = 24
    if _page_num != 1:
        # 每次ajax加载的数量
        _count_in_one_page = 15
    _paginator = Paginator(_page_num, _count_in_one_page, _total_count)

    # _hdl.order_by('-post_time')

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
    if _page_num == 1:
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
        _ret = {
            'status' : 0,
            'msg' : '没有更多数据'
        }

        if _selection_list:
            _t = loader.get_template('main/partial/selection_item_list.html')
            _c = RequestContext(request, {
                'selection_list': _selection_list,
            })
            _data = _t.render(_c)

            _ret = {
                'status' : '1',
                'data' : _data
            }
        return JSONResponse(data=_ret)
        # return HttpResponse(json.dumps(_ret))

def popular(request, template='main/popular.html'):
    _user = get_request_user(request.user.id)
    _user_context = get_request_user_context(_user)
    _group = request.GET.get('group', 'd')  # d, w, m

    # 先用精选数据来模拟热门 TODO
    _entity_id_list = [x['entity_id'] for x in NoteSelection.objects.all()[0:30]]
    _popular_list = []

    for _id in _entity_id_list:
        _entity = Entity(_id)
        _entity_context = _entity.read()
        _is_user_already_like = user_already_like_entity(request.user.id, _id)

        _popular_list.append({
            'is_user_already_like' : _is_user_already_like,
            'entity_context' : _entity_context,
        })

    return render_to_response(
        template,
        {
            'main_nav_deliver' : 'popular',
            'group' : _group,
            'user_context' : _user_context,
            'recent_time' : '10小时前',
            'popular_list' : _popular_list
        },
        context_instance=RequestContext(request)
    )


def discover(request, template='main/discover.html'):
    _user = get_request_user(request.user.id)
    _user_context = get_request_user_context(_user)

    # 先用精选数据来模拟 TODO
    _product_list = map(lambda x: Entity(x['entity_id']).read(), NoteSelection.objects[0:10])

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
        _user = get_request_user(request.user.id)
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
        _user = get_request_user(request.user.id)
        _user_context = _user.read()

        # TODO

        return render_to_response(
            template,
            {
                'user_context': _user_context,
            },
            context_instance = RequestContext(request)
        )
