from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.utils.log import getLogger

from base.entity import Entity
from web.views.util import user_entity

log = getLogger('django')

COUNT = 60


def category(request, cid, template="category/category.html"):
    # if request.is_ajax():
    #     if request.method == "GET":
    #         _page = request.GET.get('p', 1)
    #         _eids = Entity.find(
    #             category_id=cid,
    #             status='normal',
    #             offset=_page,
    #             count=COUNT,
    #         )
    #     return HttpResponse("OK")


    _page = request.GET.get('p', 1)
    _uid = request.user.id
    _eids = Entity.find(
                    category_id = cid,
                    status = 'normal',
                    offset= _page,
                    count= COUNT)

    entities = map(lambda x: user_entity(_uid, x), _eids)

    return render_to_response(template,
        {
            "category_id": cid,
            "entities" : entities,
        },
        context_instance = RequestContext(request))