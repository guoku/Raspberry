# coding=utf8
from common.entity import RBEntity
from mobile.lib.http import SuccessJsonResponse, ErrorJsonResponse


class RBMobileEntity(RBEntity):
    
    def __init__(self, entity_id):
        RBEntity.__init__(self, entity_id)

    def read(self):
        _context = super(RBMobileEntity, self).read()
        _context['created_time'] = _context["created_time"].strftime("%Y-%m-%d %H:%M:%S")
        _context['updated_time'] = _context["updated_time"].strftime("%Y-%m-%d %H:%M:%S")
        return _context



def category_entity(request, category_id):
    _entity_id_list = RBEntity.find(
        category_id = category_id
    )
    _rslt = []
    for _entity_id in _entity_id_list:
        _entity = RBMobileEntity(_entity_id)
        _rslt.append(
            _entity.read()
        )
        
    return SuccessJsonResponse(_rslt)



