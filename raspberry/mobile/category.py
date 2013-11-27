# coding=utf8
from lib.entity import MobileEntity
from lib.note import MobileNote
from lib.user import MobileUser
from base.category import Category
from mobile.lib.http import SuccessJsonResponse, ErrorJsonResponse
from mobile.models import Session_Key

def all_category(request):
    _all_categories = Category.all_group_with_full_category()
    return SuccessJsonResponse(_all_categories)

def category_stat(request, category_id):
    if request.method == "GET":
        _session = request.GET.get('session', None)
        if _session != None:
            _request_user_id = Session_Key.objects.get_user_id(_session)
        else:
            _request_user_id = None

        _rslt = {
            'entity_count' : MobileEntity.count(category_id = category_id),
            'entity_note_count' : MobileNote.count(category_id = category_id),
        }
        if _request_user_id != None:
            _rslt['like_count'] = MobileUser(_request_user_id).entity_like_count(category_id = category_id)
        else:
            _rslt['like_count'] = 0 
            
        return SuccessJsonResponse(_rslt)

