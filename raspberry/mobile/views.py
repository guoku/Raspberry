# coding=utf8
from account import *
from category import *
from entity import *


def homepage(request):
    _rslt = {}
    _rslt['banner_lit'] = [{}]
    _rslt['hot'] = []
    _rslt['hot'].append(RBCategory(1).read())
    _rslt['hot'].append(RBCategory(2).read())
    _rslt['hot'].append(RBCategory(3).read())
         
    return SuccessJsonResponse(_rslt)
     
