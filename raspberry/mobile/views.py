# coding=utf8
from account import *
from candidate import *
from category import *
from entity import *
from note import *
from user import *


def homepage(request):
    _rslt = {}
    _rslt['banner_list'] = [{}]
    _rslt['hot'] = []
    _rslt['hot'].append(RBCategory(103).read())
    _rslt['hot'].append(RBCategory(4).read())
    _rslt['hot'].append(RBCategory(83).read())
    _rslt['hot'].append(RBCategory(12).read())
    _rslt['hot'].append(RBCategory(91).read())
    _rslt['hot'].append(RBCategory(65).read())
    _rslt['hot'].append(RBCategory(116).read())
    _rslt['hot'].append(RBCategory(85).read())
    _rslt['hot'].append(RBCategory(10).read())
    
    return SuccessJsonResponse(_rslt)
     
