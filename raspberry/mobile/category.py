# coding=utf8
from common.category import RBCategory
from mobile.lib.http import SuccessJsonResponse, ErrorJsonResponse

def all_category(request):
    _all_categories = RBCategory.all_group_with_full_category()
    return SuccessJsonResponse(_all_categories)

