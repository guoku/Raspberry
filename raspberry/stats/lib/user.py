#encoding=utf8
from base.user import User 
from datetime import datetime
from django.contrib.auth.models import User as AuthUser
from django.db.models import Count
class UserStats(object):

    @classmethod 
    def new_user_count(cls,start_time, end_time = datetime.now(), group = None):
        ##返回的数据格式：[{'count':12,'date':"2012-01"}],date可能不存在
        _hd1 = AuthUser.objects.filter(date_joined__range = (start_time, end_time)) 
        if group == None:
            count = _hd1.count()
            d = {'count':count}
            return [d]
        else:
            #_hd1.extra(select = {group : group+'(date_joined)'}).values(group)
            #        .annotate(available = Count('date_joined'))
            group = group.lower()
            df = date_fromat("date_joined", group)
            _hd1 = _hd1.objects.extra(select = {"date" : df})
                        .values("date").annotate(count = Count('date_joined'))
        return list(_hd1.all())


def date_fromat(field, group):
    d = ""
    if group == "year":
        d = """DATE_FORMAT({0}, '%%Y')"""
    elif group == "month":
        d = """DATE_FORMAT({0}, '%%Y-%%m')"""
    elif group == "day":
        d = """DATE_FORMAT({0}, '%%Y-%%m-%%d')"""
    elif group == "hour":
        d = """DATE_FORMAT({0}, '%%Y-%%m-%%d-%%H')"""
    else:
        d = """DATE_FORMAT({0}, '%%x-%%m-%%v')"""
    return d.format(field)





        
