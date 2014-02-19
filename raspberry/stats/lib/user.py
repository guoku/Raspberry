#encoding=utf8
from base.models import User_Follow as FollowModel 
from datetime import datetime
from django.contrib.auth.models import User as AuthUser
from django.db.models import Count
import time
class UserStats(object):

    @classmethod 
    def new_user_count(cls,start_time, end_time = datetime.now(), group = None):
        ##返回的数据格式：[{'count':12,'timestamp':"2012-01"}],date可能不存在
        _hd1 = AuthUser.objects.filter(date_joined__range = (start_time, end_time)) 
        if group == None:
            count = _hd1.count()
            d = {'count':count}
            return [d]
        else:
            #_hd1.extra(select = {group : group+'(date_joined)'}).values(group)
            #        .annotate(available = Count('date_joined'))
            group = group.lower()
            df = date_format("date_joined", group)
            _hd1 = _hd1.extra(select = {"timestamp" : df})\
                        .values("timestamp").annotate(count = Count('date_joined'))
            result = list(_hd1.all())
            if group == "week":
                result = week_reformat(result)
            return result.reverse()
    @classmethod 
    def new_follow_count(cls, start_time, end_time = datetime.now(),
                        group = None):
        _hd1 = FollowModel.objects.filter(followed_time__range = \
                                        (start_time, end_time))

        if group == None:
            count = _hd1.count()
            d = {"count" : count}
            return [d]
        else:
            group = group.lower()
            df = date_format("followed_time", group)
            _hd1 = _hd1.extra(select = {"timestamp" : df})\
                    .values("timestamp").annotate(count = Count("followed_time"))
            
            result = list(_hd1.all())
            if group == "week":
                result= week_reformat(result)
            return result


def week_reformat(result):
    for i in range(len(result)):
        w = result[i]['timestamp']+'-1'
        t = time.strptime(w,'%Y-%W-%w')
        result[i]['timestamp'] = '%d-%d-%d'%(t.tm_year, t.tm_mon, t.tm_mday)
    return result
def date_format(field, group):
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
        d = """DATE_FORMAT({0}, '%%x-%%u')"""
    return d.format(field)





        
