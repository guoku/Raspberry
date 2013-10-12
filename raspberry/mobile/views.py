# coding=utf8
from account import *
from category import *
from entity import *


def homepage(request):
    _rslt = {}
    _rslt['banner_list'] = [{}]
    _rslt['hot'] = []
    _rslt['hot'].append(RBCategory(8).read())
    _rslt['hot'].append(RBCategory(9).read())
    _rslt['hot'].append(RBCategory(10).read())
         
    return SuccessJsonResponse(_rslt)
     
