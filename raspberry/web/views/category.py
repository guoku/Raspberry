# from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.utils.log import getLogger

from base.entity import Entity

log = getLogger('django')

COUNT = 60

def category(request, cid, template="category/category.html"):
    _page = request.GET.get('p', 1)
    _eids = Entity.find(
                    category_id = cid,
                    status = 'normal',
                    offset= int(_page),
                    count= COUNT)

    entities = map(lambda x: Entity(x).read(), _eids)
    log.info(entities)
    # for eid in _eids:
    #     log.info(Entity(eid).read())

    return render_to_response(template,
        {
            "category_id": cid,
            "entities" : entities,
        },
        context_instance = RequestContext(request))