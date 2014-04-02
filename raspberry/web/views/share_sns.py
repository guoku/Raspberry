from django.views.generic import View
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.exceptions import PermissionDenied


from base.entity import Entity
from web.forms.share_sns import ShareFrom

class WeiboView(View):

    def get(self, request):
        try:
            entity_hash = request.GET['hash']
            # return HttpResponse(entity_hash)
        except KeyError:
            raise PermissionDenied

        _entity_id = Entity.get_entity_id_by_hash(entity_hash)
        _entity_context = Entity(_entity_id).read()
        _forms = ShareFrom()

        return render_to_response('shared/weibo.html',
                            {
                                'forms': _forms,
                                'entity_context':_entity_context,
                             },
                            context_instance = RequestContext(request),)
        # return HttpResponse(_entity_context['chief_image']['url'])

    def post(self, request):


        return HttpResponse("shared ok")


__author__ = 'edison7500'
